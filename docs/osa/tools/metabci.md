# MetaBCI Tools

The MetaBCI assistant provides tools for documentation retrieval, knowledge search, and code docstring search for MetaBCI,
a Python-based open-source platform for Brain-Computer Interface (BCI) research covering Motor Imagery (MI), P300, and Steady-State Visual Evoked Potential (SSVEP) paradigms.

## Overview

| Tool | Type | Description |
|------|------|--------------|
| `retrieve_metabci_docs` | Document retrieval | Fetch MetaBCI tutorials and API reference pages |
| `search_metabci_discussions` | Knowledge search | Search GitHub issues and PRs |
| `list_metabci_recent` | Knowledge search | List recent GitHub activity |
| `search_metabci_papers` | Knowledge search | Search academic papers |
| `search_metabci_code_docs` | Code docstrings | Search Python function/class documentation |
| `get_metabci_full_docstring` | Code docstrings | Fetch a symbol's complete docstring |

## Document Retrieval

### `retrieve_metabci_docs`

Fetches documentation from 13 configured sources covering the full MetaBCI architecture:
offline analysis (`brainda`), online processing (`brainflow`), and stimulus presentation (`brainstim`).

**Preloaded docs** (embedded in system prompt):

- MetaBCI Overview & Quickstart

**On-demand docs (12):** organized by category:

- **Brainda data handling (3):** dataset loaders (BCI Competition, PhysioNet, and modifiers),
  paradigm definitions (MI, SSVEP, P300),
  utilities and I/O (EDF, GDF, `.mat` formats, channel selection)
- **Brainda algorithms (4):** decomposition
  (Common Spatial Patterns (CSP), Source Power Comodulation (SPoC),
  Filter Bank CSP (FBCSP), Task-Related Component Analysis (TRCA),
  Canonical Correlation Analysis (CCA), Multiset CCA (MsetCCA)),
  deep learning models (EEGNet, ShallowConvNet, DeepConvNet),
  manifold learning (Riemannian geometry, tangent space mapping),
  transfer learning (Manifold Embedded Knowledge Transfer (MEKT), domain adaptation)
- **Brainflow online system (3):** amplifier and hardware interfaces,
  workers and streaming (ring buffers, threading), logger configuration
- **Brainstim stimulus presentation (2):** paradigm UI implementation (PsychoPy-based SSVEP/P300/MI stimuli),
  framework core (screen management, event loops, marker synchronization)

All documentation sources point to `metabci.readthedocs.io`.

## Knowledge Search Tools

These tools search the MetaBCI community's synced knowledge database.

### `search_metabci_discussions`

Search GitHub issues and PRs in the MetaBCI repository.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `include_issues` | `bool` | `True` | Include issues in results |
| `include_prs` | `bool` | `True` | Include pull requests |
| `limit` | `int` | `5` | Maximum results |

**Tracked repository:**

- `TBC-TJU/MetaBCI`

### `list_metabci_recent`

List recent GitHub activity ordered by creation date.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `item_type` | `str` | `"all"` | Filter: `"all"`, `"issue"`, or `"pr"` |
| `repo` | `str \| None` | `None` | Filter by repository |
| `status` | `str \| None` | `None` | Filter: `"open"` or `"closed"` |
| `limit` | `int` | `10` | Maximum results |

### `search_metabci_papers`

Search academic papers related to MetaBCI and its underlying algorithms.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `5` | Maximum results |

**Tracked citation DOI:**

- `10.1016/j.pneurobio.2024.102606` (Xu et al. 2024, MetaBCI platform paper)

## Code Docstring Search

### `search_metabci_code_docs`

Search Python docstrings extracted from the MetaBCI codebase, covering
functions, classes, and methods across `brainda`, `brainflow`, and
`brainstim`.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query (e.g., `"CSP"`, `"ProcessWorker"`) |
| `limit` | `int` | `5` | Maximum results |

**Indexed repository:**

| Repository | Branch | Languages |
|-----------|--------|-----------|
| `TBC-TJU/MetaBCI` | `master` | Python |

### `get_metabci_full_docstring`

Fetch the complete stored docstring (up to about 10,000 characters) for one symbol.
Use this as a follow-up to `search_metabci_code_docs` when the returned snippet is truncated
and the user is asking about specific outputs, parameters, or examples.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `symbol_name` | `str` | required | Exact symbol name (case-insensitive), e.g. `"ProcessWorker"` |

Returns up to 5 matches when the same symbol name appears in more than
one tracked repository.

## Sync Schedule

| Source | Schedule | Notes |
|--------|----------|-------|
| GitHub | Daily, 2:00 UTC | Issues and PRs |
| Papers | Weekly, Sun 3:00 UTC | From OpenALEX, Semantic Scholar, PubMed |
| Docstrings | Weekly, Mon 4:00 UTC | Python docstrings from the MetaBCI repository |

See [Knowledge Sync](../knowledge-sync.md) for CLI commands and setup instructions.
