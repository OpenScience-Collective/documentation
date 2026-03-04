# MNE-Python Tools

The MNE-Python assistant provides tools for documentation retrieval, knowledge search, code docstring search, and Discourse forum search.

## Overview

| Tool | Type | Description |
|------|------|-------------|
| `retrieve_mne_docs` | Document retrieval | Fetch MNE tutorials and guides |
| `search_mne_discussions` | Knowledge search | Search GitHub issues and PRs |
| `list_mne_recent` | Knowledge search | List recent GitHub activity |
| `search_mne_papers` | Knowledge search | Search academic papers |
| `search_mne_code_docs` | Code docstrings | Search Python function documentation |
| `search_mne_forum` | Forum search | Search Discourse forum topics |

## Document Retrieval

### `retrieve_mne_docs`

Fetches documentation from 31 configured MNE sources, covering the full M/EEG analysis pipeline from data import through source estimation.

**Preloaded docs** (embedded in system prompt):

- MNE Cookbook (typical M/EEG workflow)
- MNE Tools Suite (ecosystem overview)

**On-demand docs (29):** organized by category:

- **Introduction (3):** overview, Python concepts, raw data structure
- **I/O (3):** reading raw data, reading epoched data, reading forward/inverse
- **Raw (2):** interactive raw data visualization, filtering
- **Preprocessing (5):** regression-based artifact removal, ICA, Signal Space Projection (SSP), Maxwell filtering, repairing bad channels
- **Epochs (3):** creating epochs, handling metadata, visualizing epochs
- **Evoked (2):** creating evoked objects, whitening evoked data
- **Time-frequency (2):** frequency/time-frequency analysis, spectral connectivity
- **Forward (2):** head model and forward computation, source space
- **Inverse (3):** Minimum Norm Estimates (MNE), dynamic Statistical Parametric Mapping (dSPM), beamformers
- **Statistics (2):** spatiotemporal cluster permutation, sensor-space statistics
- **Machine learning (1):** decoding with MNE and scikit-learn
- **Clinical (1):** sleep staging with MNE

All documentation sources point to rendered HTML pages on `mne.tools/stable/` which are automatically converted to markdown by the fetcher.

## Knowledge Search Tools

These tools search the MNE community's synced knowledge database.

### `search_mne_discussions`

Search GitHub issues and PRs across MNE repositories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `include_issues` | `bool` | `True` | Include issues in results |
| `include_prs` | `bool` | `True` | Include pull requests |
| `limit` | `int` | `5` | Maximum results |

**Tracked repositories:**

- `mne-tools/mne-python`
- `mne-tools/mne-bids`
- `mne-tools/mne-connectivity`
- `mne-tools/mne-icalabel`
- `mne-tools/mne-lsl`

### `list_mne_recent`

List recent GitHub activity ordered by creation date.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `item_type` | `str` | `"all"` | Filter: `"all"`, `"issue"`, or `"pr"` |
| `repo` | `str \| None` | `None` | Filter by repository |
| `status` | `str \| None` | `None` | Filter: `"open"` or `"closed"` |
| `limit` | `int` | `10` | Maximum results |

### `search_mne_papers`

Search academic papers related to MNE-Python.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `5` | Maximum results |

**Tracked citation DOIs:**

- `10.3389/fnins.2013.00267` (Gramfort et al. 2013, main MNE paper)
- `10.1016/j.neuroimage.2013.10.027` (Gramfort et al. 2014)
- `10.21105/joss.01896` (MNE-BIDS)
- `10.21105/joss.04484` (MNE-ICALabel)
- `10.21105/joss.08088` (MNE-LSL)

## Code Docstring Search

### `search_mne_code_docs`

Search Python docstrings extracted from MNE ecosystem repositories. Covers functions, classes, and methods across all 5 tracked repos.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query (e.g., "read_raw_edf", "Epochs") |
| `limit` | `int` | `5` | Maximum results |

**Tracked repositories (Python only):**

- `mne-tools/mne-python` (800+ Python files)
- `mne-tools/mne-bids`
- `mne-tools/mne-connectivity`
- `mne-tools/mne-icalabel`
- `mne-tools/mne-lsl`

## Discourse Forum Search

### `search_mne_forum`

Search topics from the MNE Discourse forum ([mne.discourse.group](https://mne.discourse.group)). Returns topic titles, post previews, accepted answers, and direct links.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `category` | `str \| None` | `None` | Filter by Discourse category |
| `limit` | `int` | `5` | Maximum results |

The forum database is synced weekly from the Discourse public API (6000+ topics, 30000+ posts). Topics include the first post and the accepted answer (or highest-voted reply).

## Sync Schedule

| Source | Schedule | Notes |
|--------|----------|-------|
| GitHub | Weekly, Mon 2:30 UTC | Issues and PRs from 5 repos |
| Papers | Weekly, Mon 3:30 UTC | From OpenALEX, Semantic Scholar, PubMed |
| Docstrings | Weekly, Mon 4:30 UTC | Python docstrings from 5 repos |
| Discourse | Weekly, Mon 5:30 UTC | Forum topics with patient rate limiting (1 req/s) |
