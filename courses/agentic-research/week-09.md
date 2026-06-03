# Week 9: Neuroinformatics -- Standards, Sharing, and Credit

## Overview

A finished analysis is not a finished contribution. The data behind it has to be reproducible, shareable, and citable, or the work dies with the paper. Two standards carry the weight: the Brain Imaging Data Structure (BIDS) answers where everything lives (structure), and Hierarchical Event Descriptors (HED) answer what every event meant (semantics). The single most useful idea this week: the bar for a complete annotation is concrete and falsifiable. **A language model should be able to reconstruct the stimulus, or the experiment, from the annotation alone.** That is not a metaphor; it is exactly the test demonstrated in the Healthy Brain Network EEG (HBN-EEG) paper (Shirazi et al., 2024, Figure 9), where Claude Sonnet 3.5 regenerated the Surround Suppression stimulus from its HED description with no image.

The dataset throughout is HBN-EEG, the very data the course has analyzed since Week 3. It is itself a BIDS + HED dataset published on both OpenNeuro and NEMAR with exactly the tools this session teaches: the loop closes, the data you analyzed is the worked example for how to share data.

!!! abstract "Learning Objectives"
    - Frame data sharing as three locks: **structure, semantics, and credit**
    - Read a **BIDS** dataset: directory layout, JSON sidecars, `events.tsv`, `participants.tsv`
    - Understand **HED** as the semantics layer: hierarchical, composable, validatable tags in an `events.json` sidecar
    - Apply the **recreate-the-stimulus bar**: an annotation is complete when a language model can rebuild the stimulus from it alone
    - Use **HEDit** to turn a rich prose description into validated HED (Parser to Tagger to Validator)
    - Use **`/neuroinformatics:bids-conversion`** and the **`bids-validator` agent** (the mechanical defence) to produce a valid dataset
    - Share with **OpenNeuro** and **NEMAR**; use **`nemar-cli`** for trivial validation, a private-repo collaboration workflow, and DOIs with **ORCID auto-linking**
    - Read a real **DataCite metadata gap**: the same dataset on NEMAR vs OpenNeuro

<div class="embed-container">
  <iframe
    src="https://www.youtube.com/embed/placeholder-week-09"
    title="Week 9: Neuroinformatics -- Standards, Sharing, and Credit"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>


## Slides

<div class="embed-container">
  <iframe
    src="../../slides/agentic-research/week-09/presentation.html?presentation=./week-09.json"
    title="Week 9 Slides"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>

<p class="slide-hint">Use arrow keys to navigate. Press <kbd>F</kbd> for fullscreen, <kbd>?</kbd> for shortcuts.</p>


---

## Guide

The rest of this page walks through the workflow in the order the live session follows.

### 1. The Reuse-and-Credit Gap

A lab collects dense, synchronized data. What reaches re-users is a thin `events.tsv` with one cryptic column and a results figure locked in a folder. Three locks snap shut at once.

![A rich raw recording funnels down to a thin shared artifact, with three padlocks: structure, semantics, and credit](../../slides/agentic-research/week-09/assets/icons/reuse-credit-gap.svg){ .figure-diagram }

- **Structure** -- where is everything? Custom layouts mean every re-user writes glue code first.
- **Semantics** -- what did the events mean? A numeric event code is meaningless outside the lab.
- **Credit** -- who is cited when it is reused? Without a DOI and author identifiers, reuse traces back to no one.

!!! quote "Analysis-ready means no forensic search for unreported details"
    The information is not lost; it just never reaches the shared artifact. BIDS, HED, and good sharing close the three locks.

### 2. Two Standards, One Bar

**BIDS answers where; HED answers what.** The bar that judges both is the same: someone, or a language model, can reconstruct your experiment without emailing you.

- **BIDS (Brain Imaging Data Structure)** -- a filesystem convention plus metadata. *Structure.*
- **HED (Hierarchical Event Descriptors)** -- a controlled, composable, validatable event vocabulary. *Semantics.*

### 3. BIDS: One Layout, Every Dataset

A filesystem convention plus metadata: predictable names (`sub-`, `ses-`, `task-`), JSON sidecars, and TSV tables.

![An annotated BIDS directory tree for one HBN-EEG subject](../../slides/agentic-research/week-09/assets/icons/bids-tree.svg){ .figure-diagram }

A BIDS dataset is readable by EEGLAB, MNE-Python, the BIDS validator, and BIDS Apps, and it is the upload format both OpenNeuro and NEMAR expect. Standard structure is also what makes mega-analysis across studies possible. The payoff is leverage, not bureaucracy.

### 4. Where Structure Ends

The JSON sidecar carries acquisition metadata; `events.tsv` carries the timeline.

```json
{
  "TaskName": "surroundSupp",
  "SamplingFrequency": 500,
  "EEGReference": "Cz",
  "PowerLineFrequency": 60,
  "EEGChannelCount": 128
}
```

```text
onset    duration   value
0.000    n/a        12
1.500    n/a        14
3.000    n/a        12
```

Structure tells you **where** an event sits on the timeline. It cannot tell you **what** the event was. That gap is semantics.

### 5. HED: the Semantics Standard

`events.tsv` is thin: an onset and a cryptic numeric code. Stimulus, modality, condition, response, context -- all real, all recorded, none of it in the shared file. (HBN originally shipped numeric codes; the first curation step replaced them with meaningful strings, then annotated with HED.)

One HED tag is a comma-separated path through a controlled schema; the hierarchy carries meaning, so analysis works at any level:

```text
Action, Move, Move-body-part, Move-upper-extremity, Press
```

![HED anatomy: a tag as a schema path, the inheritance tree, and the events.json sidecar pattern](../../slides/agentic-research/week-09/assets/icons/hed-anatomy.svg){ .figure-diagram }

You can analyze at the leaf (`Press`) or any ancestor (`Move`). The sidecar pattern keeps `events.tsv` unchanged; all semantics live in `events.json` under HED keys.

### 6. The Bar: Recreate the Stimulus

In the HBN-EEG paper, the HED annotation of the Surround Suppression task was handed to Claude Sonnet 3.5 with **no image**, and the model regenerated the visual stimulus from the annotation alone.

![HBN-EEG Figure 9: the intended Surround Suppression stimulus and Claude's regeneration from the HED annotation alone, with what matched and the one miss](../../slides/agentic-research/week-09/assets/icons/recreate-the-stimulus-figure.svg){ .figure-diagram }

Everything structural came back correct: the gratings, the vertical-grating background, central fixation, the contrast relationship, four disks present. The **only** miss was the disks' **size and position** -- both awkward to express in HED, so they were left out, and the model had no way to reproduce them.

!!! important "The completeness test"
    If a language model can rebuild your stimulus from the annotation alone, the annotation is complete. If it can't, you left something out. That honest miss is also a real lesson: HED nails event semantics, but spatial geometry is hard to encode.

Cite: Shirazi et al. (2024), *HBN-EEG: The FAIR implementation of the Healthy Brain Network EEG dataset*, bioRxiv [10.1101/2024.10.03.615261](https://doi.org/10.1101/2024.10.03.615261).

### 7. HEDit: AI-assisted HED

HED workflows stall for most labs, and it is a workflow problem, not a willingness problem: roughly 2000 tags, expert-only fluency, a validator with cryptic messages.

![HEDit pipeline: Parser, Tagger, Validator with a feedback loop](../../slides/agentic-research/week-09/assets/icons/hedit-pipeline.svg){ .figure-diagram }

[HEDit](https://github.com/Annotation-Garden/HEDit) turns the wall into a paragraph. You write one rich prose description per event value; a Parser to Tagger to Validator pipeline (LangGraph, with the official HED validator in the loop) returns a BIDS-compliant `events.json` with HED plus a provenance trail. The schema is the contract; no agent invents vocabulary. And HEDit is only as good as the description: it is tuned for exactly the detail the recreate-the-stimulus bar demands.

### 8. The neuroinformatics Plugin: 2 Skills + 1 Agent

- **`/neuroinformatics:bids-conversion`** -- a guided conversion to BIDS.
- **`bids-validator`** (agent) -- autonomous validation and fixes. This week's mechanical defence.
- **`/neuroinformatics:experiment-design`** -- the data-collection side (PsychoPy + Lab Streaming Layer); in the plugin, not today's focus.

A guided six-step conversion ends where the next act begins, validation:

```text
1. Inventory  ->  2. Scaffold  ->  3. Convert files  ->  4. JSON sidecars  ->  5. TSV tables  ->  6. Validate
```

Modalities: EEG, EMG, MEG, fMRI, and behavioral data.

### 9. The bids-validator Agent: the Mechanical Defence

The agent runs the BIDS validator, categorizes findings, applies fixes with confirmation, re-validates, and reports readiness.

```text
## BIDS Validation Report
Subjects: 12   Modalities: eeg
Errors fixed: 2
  [FIXED] missing dataset_description.json
  [FIXED] _eeg.json missing PowerLineFrequency -> 60
Remaining warnings: 2
Ready for submission: YES
```

!!! note "Two checks by design"
    The agent fixes your data **locally**; `nemar-cli` validates again **at the upload gate**. This is Week 9's `cite-the-card` / `validate_fonts.py`: a deterministic gate that turns "looks fine" into pass/fail.

### 10. Sharing: OpenNeuro and NEMAR

[OpenNeuro](https://openneuro.org) is the de-facto open BIDS archive: validated on ingest, public, DOI-minted.

!!! warning "Honest caveats"
    Private upload *is* possible on OpenNeuro, but only via the command line / direct push (no polished GUI), and the DOI record stays sparse: no ORCID author links, minimal metadata.

[NEMAR](https://nemar.org) specializes in EEG/MEG BIDS datasets and sits next to San Diego Supercomputer Center compute, so you can analyze without downloading. HBN-EEG lives on both.

### 11. nemar-cli: Validation, Upload, Publish

Validation is one command, and also runs automatically on upload and on every update pull request:

```bash
nemar dataset validate ./my-dataset
```

The full path, and the collaboration model:

```bash
nemar auth login                          # one-time, API key cached
nemar dataset validate ./my-dataset       # BIDS check, must pass
nemar dataset upload ./my-dataset         # creates a private GitHub repo
nemar dataset publish request nm000XXX    # admin approves -> public + DOI
```

`upload` creates a **private GitHub repository where you are the admin**: invite collaborators and push directly while you stage. After publishing, changes go through pull requests and version tags. (OpenNeuro also supports private upload, just command-line only, so the NEMAR advantage is this collaboration model plus the rich DOI metadata, not "private vs public.")

### 12. DOI Minting + ORCID Auto-link

![DOI minting and ORCID auto-linking: authors to ORCID iDs to DataCite DOI to each author's ORCID record](../../slides/agentic-research/week-09/assets/icons/doi-orcid.svg){ .figure-diagram }

On publish, `nemar-cli` mints a **concept DOI** (one stable citation across all versions) plus per-version DOIs, via EZID writing DataCite kernel-4 metadata (the DOIs carry the `10.82901/NEMAR.<id>` prefix), and **auto-links every author's ORCID iD**. The dataset then appears on each author's ORCID record automatically. OpenNeuro does not link authors to ORCID on the DOI yet.

### 13. The Metadata Gap: Proof on a Real Dataset

Live DataCite data, the same HBN-EEG Release 1, the same eight authors, two homes.

![DataCite metadata comparison: NEMAR nm000103 vs OpenNeuro ds005505, grouped into findability and credit fields](../../slides/agentic-research/week-09/assets/icons/doi-metadata-gap.svg){ .figure-diagram }

| DataCite field | NEMAR `nm000103` | OpenNeuro `ds005505` |
|---|---|---|
| Stable concept DOI | yes | no (version-only) |
| **Authors linked to ORCID iD** | **8 / 8** | **0 / 8** |
| License | CC-BY-NC-SA-4.0 | none |
| Subject keywords | 8 | 0 |
| Description / abstract | yes | none |
| Links to papers + related datasets | 5 | 0 |
| Funding references | 2 | 0 |

!!! success "Findability and credit are metadata, not luck"
    OpenNeuro's DOI record carries only a title and author names; NEMAR fills every field. (Source: `api.datacite.org`, live records.)

### 14. Live Walkthrough

Two small, honest actions, about four minutes total:

1. **HEDit** -- write one rich prose description of an HBN event and watch it become a validated HED string.
2. **`nemar dataset validate`** -- run it on the HBN practicum dataset and read the clean BIDS report.

!!! important "We do not manufacture a pass"
    If validation surfaces something, we walk it on stage.

### 15. Before Next Week

- Install [`research-skills`](https://github.com/neuromechanist/research-skills); it bundles `neuroinformatics`, `figures`, `manuscript`, `opencite`, `grant`, `project`, and `presentation`.
- If you have a small EEG/EMG dataset, try `/neuroinformatics:bids-conversion` and run the `bids-validator` agent.
- Browse HBN-EEG on [NEMAR](https://nemar.org) and [OpenNeuro](https://openneuro.org); compare the two DOI records on [DataCite Commons](https://commons.datacite.org).
- Optional: try [HEDit](https://github.com/Annotation-Garden/HEDit) on one event from your own experiment, written as a rich paragraph.

Week 10 is the capstone: building your own plugin.

---

## Resources

**Course materials**

- [Week 9 session](https://github.com/OpenScience-Collective/agentic-research-course/tree/main/sessions/week-09)
- [Week 9 blog (markdown source)](https://github.com/OpenScience-Collective/agentic-research-course/blob/main/blog/week-09-neuroinformatics.md)
- [Course repository](https://github.com/OpenScience-Collective/agentic-research-course)
- [research-skills plugin](https://github.com/neuromechanist/research-skills) (bundles `neuroinformatics`, `figures`, `manuscript`, `opencite`, `grant`, `project`, `presentation`)

**Standards and tools**

- [BIDS specification](https://bids-specification.readthedocs.io/) (Brain Imaging Data Structure)
- [HED (Hierarchical Event Descriptors)](https://www.hedtags.org/)
- [HEDit](https://github.com/Annotation-Garden/HEDit) (natural language to validated HED)
- [nemar-cli](https://nemar-cli.pages.dev) (upload, validate, version, and publish to NEMAR)
- [OpenNeuro](https://openneuro.org) and [NEMAR](https://nemar.org) (open BIDS archives)
- [DataCite Commons](https://commons.datacite.org) (inspect DOI metadata)
- [ORCID](https://orcid.org/) (researcher and contributor identifiers)

**Reference**

- Shirazi et al. (2024), *HBN-EEG: The FAIR implementation of the Healthy Brain Network EEG dataset*, bioRxiv [10.1101/2024.10.03.615261](https://doi.org/10.1101/2024.10.03.615261)
- [Open Science Collective Discord](https://discord.gg/5dWJCUmUww)

<style>
.embed-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
.embed-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}
.slide-hint {
  margin: -0.5rem 0 1.5rem 0;
  font-size: 0.75rem;
  color: var(--md-default-fg-color--lighter);
}
.slide-hint kbd {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 3px;
  background: var(--md-code-bg-color);
}
.figure-diagram {
  display: block;
  width: 100%;
  height: auto;
  max-width: 920px;
  margin: 1rem auto;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 6px;
  padding: 0.5rem;
  background: #ffffff;
}
</style>
