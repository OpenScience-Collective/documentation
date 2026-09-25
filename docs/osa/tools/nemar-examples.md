# NEMAR Examples: a Power Spectrum and an Event-Related Potential Image

The NEMAR assistant can analyze a recording for you in your browser.
This page shows two analyses on ERP CORE (`nm000132`), a set of standard event-related potential (ERP) paradigms:
the power spectrum of a recording's electroencephalography (EEG) channels, and an ERP image of its conditions.
The recording is subject 001's N170 task, which shows faces, cars, scrambled faces and scrambled cars, 80 of each.

## How to use it

1. Open a dataset's page on [nemar.org](https://nemar.org), for example [nm000132](https://nemar.org/dataset/nm000132).
2. Open the assistant and ask a question, or pick one of its suggestions, for example:
    - "Show the power spectrum of the EEG channels in sub-001's N170 recording from nm000132"
    - "Plot an ERP image of faces against scrambled faces at PO8 in sub-001's N170 recording from nm000132"
3. The assistant looks up the recording and its events, then writes the code. Read it, and approve it to run.
4. The figure appears in the chat.

Any dataset with a Zarr copy works the same way: name the recording, the conditions, and the channel you want.
The assistant reads NEMAR's Zarr copy, which is lossy and may be downsampled (this recording is 250 Hz, from 1024 Hz);
for a published result, download the Brain Imaging Data Structure (BIDS) files.
For the same analyses in NEMAR's notebook or your own Python, see NEMAR's [worked examples](https://docs.nemar.org/platform/zarr/examples/).

## The power spectrum

![The power spectra of 30 EEG channels from nm000132, subject 001, N170 task, over the first two minutes, from 1 to 40 Hz on a log scale, with their median in black peaking near 11 Hz.](nemar-examples-spectrum.png)

The first two minutes of the recording, with the three electrooculography (EOG) channels left out.
The median spectrum peaks at 11 Hz, the alpha rhythm.

??? example "The code the assistant runs"

    ```python
    import eegprep_lean
    import matplotlib.pyplot as plt
    import numpy as np

    index = await eegprep_lean.read_index("nm000132")
    store = index.store("sub-001/eeg/sub-001_task-N170_eeg.set")
    group = store.group("eeg_250hz")
    window = await eegprep_lean.read_window(
        index, store, group=group, start_sample=0, n_samples=int(120 * group.rate)
    )
    labels = list(window.labels)
    eeg = [i for i, name in enumerate(labels) if "EOG" not in name.upper()]

    # Welch's method in numpy: 2-second Hann-tapered segments overlapping by half.
    rate = window.rate
    segment = int(2 * rate)
    taper = np.hanning(segment)
    x = window.data[eeg] - window.data[eeg].mean(axis=1, keepdims=True)
    starts = range(0, x.shape[1] - segment + 1, segment // 2)
    power = sum(np.abs(np.fft.rfft(x[:, s : s + segment] * taper, axis=1)) ** 2 for s in starts)
    power = power / (len(starts) * rate * np.sum(taper**2))
    power[:, 1:-1] *= 2
    freqs = np.fft.rfftfreq(segment, 1 / rate)
    band = (freqs >= 1) & (freqs <= 40)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.semilogy(freqs[band], power[:, band].T, lw=0.5, alpha=0.4)
    ax.semilogy(freqs[band], np.median(power[:, band], axis=0), color="k", lw=1.5, label="median")
    ax.set(xlabel="Frequency (Hz)", ylabel=f"Power ({window.unit}²/Hz)",
           title=f"{len(eeg)} EEG channels, first 2 minutes (EOG left out)")
    ax.legend()
    display(fig)
    ```

## The ERP image

![ERP images at PO8 for faces (79 of 80 epochs) and scrambled faces (78 of 80 epochs) from nm000132, subject 001, with the two averages and their difference below, the difference most negative near 250 ms.](nemar-examples-erp-image.png)

Each row is one epoch at PO8, from 200 ms before a stimulus to 800 ms after, and the traces below are each condition's average.
Faces are more negative than scrambled faces from about 150 ms, most near 250 ms in this subject:
about 4 µV over 150 to 260 ms.

??? example "The code the assistant runs"

    The assistant fills in each condition's event positions from NEMAR's events for this recording.

    ```python
    import eegprep_lean
    import matplotlib.pyplot as plt
    import numpy as np

    # From nemar_get_events(where={"event_type": ["face", "scrambled_face"]}, columns=["event_type"]):
    # each condition's sample_index values, at the group's 250 Hz.
    FACE = [5291, 5683, ...]  # 80 values
    SCRAMBLED_FACE = [4904, 7195, ...]  # 80 values

    index = await eegprep_lean.read_index("nm000132")
    store = index.store("sub-001/eeg/sub-001_task-N170_eeg.set")
    group = store.group("eeg_250hz")
    recording = await eegprep_lean.read_window(
        index, store, group=group, start_sample=0, n_samples=group.n_samples
    )
    labels = list(recording.labels)
    eeg = [i for i, name in enumerate(labels) if "EOG" not in name.upper()]
    rate = recording.rate

    data = recording.data[eeg].astype(float)
    data -= data.mean(axis=0)  # average reference
    # A windowed-sinc low-pass at 30 Hz, 0.4 s of taps; "same" keeps it zero-phase.
    taps = int(0.4 * rate) // 2 * 2 + 1
    kernel = np.sinc(2 * 30 / rate * (np.arange(taps) - taps // 2)) * np.hamming(taps)
    po8 = np.convolve(data[[labels[i] for i in eeg].index("PO8")], kernel / kernel.sum(), mode="same")

    pre, post = int(0.2 * rate), int(0.8 * rate)
    times = np.arange(-pre, post) / rate * 1000


    def epochs(samples):
        e = np.stack([po8[s - pre : s + post] for s in samples if s >= pre and s + post <= len(po8)])
        e -= e[:, :pre].mean(axis=1, keepdims=True)
        return e[np.abs(e).max(axis=1) <= 100]


    faces, scrambled = epochs(FACE), epochs(SCRAMBLED_FACE)
    smooth = lambda e: np.stack([e[max(0, k - 2) : k + 3].mean(axis=0) for k in range(len(e))])
    limit = np.percentile(np.abs(np.concatenate([smooth(faces), smooth(scrambled)])), 98)

    fig = plt.figure(figsize=(9, 6.5), layout="constrained")
    grid = fig.add_gridspec(2, 2, height_ratios=[3, 1.4])
    for col, (title, e) in enumerate([("Faces", faces), ("Scrambled faces", scrambled)]):
        ax = fig.add_subplot(grid[0, col])
        image = ax.imshow(smooth(e), aspect="auto", origin="lower", cmap="RdBu_r",
                          vmin=-limit, vmax=limit, extent=[times[0], times[-1], 0, len(e)])
        ax.axvline(0, color="gray", lw=0.8)
        ax.set(title=f"{title}, PO8 ({len(e)} of 80 epochs)", ylabel="Epoch" if col == 0 else None)
    fig.colorbar(image, ax=fig.axes, label=recording.unit, shrink=0.8)
    average = fig.add_subplot(grid[1, :])
    average.plot(times, faces.mean(axis=0), label="faces")
    average.plot(times, scrambled.mean(axis=0), label="scrambled faces")
    average.plot(times, faces.mean(axis=0) - scrambled.mean(axis=0), color="k", lw=1, label="difference")
    average.axvline(0, color="gray", lw=0.8)
    average.set(xlabel="Time (ms)", ylabel=recording.unit, xlim=(times[0], times[-1]))
    average.legend(fontsize=8, loc="upper left")
    display(fig)
    w = (times >= 150) & (times <= 260)
    print(f"150-260 ms at PO8: faces minus scrambled faces {faces[:, w].mean() - scrambled[:, w].mean():.1f} {recording.unit}")
    ```
