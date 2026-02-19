# EEGLAB Tools

The EEGLAB assistant provides tools for documentation retrieval, knowledge search, code docstring search, and mailing list FAQ search.

## Overview

| Tool | Type | Description |
|------|------|-------------|
| `retrieve_eeglab_docs` | Document retrieval | Fetch EEGLAB tutorials and guides |
| `search_eeglab_discussions` | Knowledge search | Search GitHub issues and PRs |
| `list_eeglab_recent` | Knowledge search | List recent GitHub activity |
| `search_eeglab_papers` | Knowledge search | Search academic papers |
| `search_eeglab_docstrings` | EEGLAB-specific | Search MATLAB/Python function documentation |
| `search_eeglab_faqs` | EEGLAB-specific | Search mailing list FAQ entries |

## Document Retrieval

### `retrieve_eeglab_docs`

Fetches documentation from 22 configured EEGLAB sources, covering installation, data import, preprocessing, ICA, visualization, group analysis, scripting, and plugin integration.

**Preloaded docs** (embedded in system prompt):

- EEGLAB quickstart (installation and basic functionality)
- Dataset management

**On-demand docs:** data import (3 docs), preprocessing (4 docs), ICA and artifacts (4 docs), epoching, visualization (4 docs), group analysis (2 docs), scripting (2 docs), and integration (2 docs: BIDS, LSL).

## Knowledge Search Tools

These tools search the EEGLAB community's synced knowledge database.

### `search_eeglab_discussions`

Search GitHub issues and PRs across EEGLAB repositories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `include_issues` | `bool` | `True` | Include issues in results |
| `include_prs` | `bool` | `True` | Include pull requests |
| `limit` | `int` | `5` | Maximum results |

**Tracked repositories:**

- `sccn/eeglab`
- `sccn/ICLabel`
- `sccn/clean_rawdata`
- `sccn/EEG-BIDS`
- `sccn/labstreaminglayer`
- `sccn/liblsl`

### `list_eeglab_recent`

List recent GitHub activity ordered by creation date.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `item_type` | `str` | `"all"` | Filter: `"all"`, `"issue"`, or `"pr"` |
| `repo` | `str \| None` | `None` | Filter by repository (e.g., `"sccn/eeglab"`) |
| `status` | `str \| None` | `None` | Filter: `"open"` or `"closed"` |
| `limit` | `int` | `10` | Maximum results |

### `search_eeglab_papers`

Search academic papers related to EEGLAB.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `5` | Maximum results |

**Tracked citation DOIs:**

- Delorme & Makeig (2004) - EEGLAB: an open source toolbox
- Pion-Tonachini et al. (2019) - ICLabel: automated EEG IC classification
- Bigdely-Shamlo et al. (2015) - PREP: standardized preprocessing

## EEGLAB-Specific Tools

### `search_eeglab_docstrings`

Search function documentation from the EEGLAB codebase. This tool searches over MATLAB and Python docstrings extracted from EEGLAB and its plugins.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Function name or description (e.g., `"pop_loadset"`, `"ICA decomposition"`) |
| `limit` | `int` | `5` | Maximum results |
| `language` | `str \| None` | `None` | Filter by language: `"matlab"` or `"python"` |

**Indexed repositories:**

| Repository | Branch | Languages |
|-----------|--------|-----------|
| `sccn/eeglab` | `develop` | MATLAB, Python |
| `sccn/ICLabel` | `master` | MATLAB |
| `sccn/clean_rawdata` | `master` | MATLAB |

**Example:**

```
User: "How do I use pop_loadset?"
Agent: calls search_eeglab_docstrings(query="pop_loadset")
Response:
  Found 1 function(s):

  **1. pop_loadset (function) - functions/popfunc/pop_loadset.m**
  Language: matlab
  [View source](https://github.com/sccn/eeglab/blob/.../pop_loadset.m#L1)

  Load an EEGLAB dataset file...
```

!!! note "Sync Required"
    Populate with `osa sync docstrings --community eeglab`.

### `search_eeglab_faqs`

Search FAQ entries generated from the EEGLAB mailing list archive (since 2004). The FAQ database is created using a two-agent LLM pipeline that evaluates thread quality and summarizes high-quality discussions.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query (topic or question) |
| `category` | `str \| None` | `None` | Filter by category (e.g., `"troubleshooting"`, `"how-to"`, `"bug-report"`) |
| `limit` | `int` | `5` | Maximum results |

**Returns:** FAQ entries with:

- Question and answer summary
- Category classification
- Quality score (0.0-1.0)
- Tags
- Link to original mailing list thread

**Example:**

```
User: "How do I remove artifacts from EEG data?"
Agent: calls search_eeglab_faqs(query="artifact removal")
Response:
  Found 3 FAQ entries:

  **1. How do I remove artifacts from my EEG data?**
  Category: how-to | Quality: 0.9/1.0
  Tags: artifacts, preprocessing, ICA

  There are several approaches to artifact removal in EEGLAB...

  [View thread](https://sccn.ucsd.edu/pipermail/eeglablist/...)
```

!!! note "Sync Required"
    Populate with `osa sync mailman --community eeglab` followed by `osa sync faq --community eeglab`.

### FAQ Generation Pipeline

The FAQ entries are generated through a two-stage LLM pipeline:

1. **Evaluation agent** - Scores each mailing list thread for quality using a fast, cost-efficient model. Threads must have at least 2 messages from 2 participants.
2. **Summary agent** - Creates structured FAQ entries (question, answer, category, tags) from threads scoring above the quality threshold (default: 0.7).

This approach filters out low-quality threads early, keeping costs manageable even for archives spanning 20+ years.

Configuration is in the community's `config.yaml` under `faq_generation`. See [Schema Reference](../registry/schema-reference.md) for details.

## Sync Configuration

The EEGLAB assistant's knowledge sync schedule:

```yaml
sync:
  github:
    cron: "0 2 * * *"       # daily at 2am UTC
  papers:
    cron: "0 3 * * 0"       # weekly Sunday at 3am UTC
  docstrings:
    cron: "0 4 * * 1"       # weekly Monday at 4am UTC
  mailman:
    cron: "0 5 * * 1"       # weekly Monday at 5am UTC
  faq:
    cron: "0 6 1 * *"       # monthly 1st at 6am UTC
```

See [Knowledge Sync](../knowledge-sync.md) for CLI commands and setup instructions.
