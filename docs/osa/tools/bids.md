# BIDS Tools

The Brain Imaging Data Structure (BIDS) assistant provides tools for documentation retrieval, knowledge search, and BIDS Extension Proposal (BEP) lookup.

## Overview

| Tool | Type | Description |
|------|------|-------------|
| `retrieve_bids_docs` | Document retrieval | Fetch BIDS specification and website docs |
| `search_bids_discussions` | Knowledge search | Search GitHub issues and PRs |
| `list_bids_recent` | Knowledge search | List recent GitHub activity |
| `search_bids_papers` | Knowledge search | Search academic papers |
| `lookup_bep` | BIDS-specific | Look up BIDS Extension Proposals |

## Document Retrieval

### `retrieve_bids_docs`

Fetches documentation from configured BIDS sources. The BIDS assistant has 49 configured documentation pages spanning the specification, website, and FAQ.

**Preloaded docs** (embedded in system prompt):

- BIDS common principles
- Getting started with BIDS

**On-demand docs** (fetched when needed): specification core, modality-specific files (MRI, EEG, MEG, iEEG, PET, NIRS, Motion, Microscopy, MRS, EMG, Behavioral, Genetics, Physiological), derivatives, getting started guides, FAQ, schema documentation, and more.

Documents are organized by category: `core`, `specification`, `modality_agnostic`, `modality_specific`, `derivatives`, `getting_started`, `faq`, `tools`, `extensions`, `schema`.

## Knowledge Search Tools

These tools search the BIDS community's synced knowledge database. They require running `osa sync` commands to populate data (see [Knowledge Sync](../knowledge-sync.md)).

### `search_bids_discussions`

Search GitHub issues and PRs across BIDS repositories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query (keywords, issue numbers) |
| `include_issues` | `bool` | `True` | Include issues in results |
| `include_prs` | `bool` | `True` | Include pull requests in results |
| `limit` | `int` | `5` | Maximum results to return |

**Tracked repositories:**

- `bids-standard/bids-specification`
- `bids-standard/bids-validator`
- `bids-standard/bids-website`
- `bids-standard/bids-examples`

**Example interaction:**

```
User: "Are there any discussions about derivatives?"
Agent: calls search_bids_discussions(query="derivatives")
Agent: "There's a related discussion: [link to actual issue]"
```

### `list_bids_recent`

List recent GitHub activity ordered by creation date.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `item_type` | `str` | `"all"` | Filter: `"all"`, `"issue"`, or `"pr"` |
| `repo` | `str \| None` | `None` | Filter by repository (e.g., `"bids-standard/bids-specification"`) |
| `status` | `str \| None` | `None` | Filter: `"open"` or `"closed"` |
| `limit` | `int` | `10` | Maximum results to return |

**Example interaction:**

```
User: "What are the latest PRs in the specification?"
Agent: calls list_bids_recent(item_type="pr", repo="bids-standard/bids-specification")
```

### `search_bids_papers`

Search academic papers related to BIDS.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `5` | Maximum results to return |

**Tracked citation DOIs:**

The BIDS assistant tracks papers citing 14 core DOIs, including:

- Gorgolewski et al. (2016) - The brain imaging data structure
- EEG-BIDS (Pernet et al., 2019)
- MEG-BIDS (Niso et al., 2018)
- iEEG-BIDS (Holdgraf et al., 2019)
- PET-BIDS (Norgaard et al., 2021)
- And 9 additional modality-specific extension papers

Papers are sourced from OpenALEX, Semantic Scholar, and PubMed.

## BIDS-Specific Tools

### `lookup_bep`

Look up BIDS Extension Proposals (BEPs) by number or keyword. BEPs are the mechanism for adding new data types to BIDS. This tool searches over synced BEP specification content from open pull requests against the BIDS specification.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | BEP number (e.g., `"032"`, `"BEP032"`) or keyword (e.g., `"neuropixels"`) |
| `limit` | `int` | `3` | Maximum results to return |

**Returns:** Formatted BEP information including:

- BEP number and title
- Current status (proposed, draft, etc.)
- Lead authors
- Links to the PR, HTML preview, and/or Google Doc
- Content snippet from the proposal

**Example:**

```
User: "Is there a BEP for eye tracking data?"
Agent: calls lookup_bep(query="eye tracking")
Response:
  Found 1 BEP(s):

  **BEP020: Eye Tracking including Gaze Position and Pupil Size**
  Status: proposed
  PR: https://github.com/bids-standard/bids-specification/pull/...
  Preview: https://bids-specification--...readthedocs.build/...
```

!!! note "Sync Required"
    The `lookup_bep` tool requires running `osa sync beps --community bids` to populate BEP data from open specification PRs.

## Sync Configuration

The BIDS assistant's knowledge sync is configured in its `config.yaml`:

```yaml
sync:
  github:
    cron: "0 2 * * *"       # daily at 2am UTC
  papers:
    cron: "0 3 * * 0"       # weekly Sunday at 3am UTC
  beps:
    cron: "0 4 * * 1"       # weekly Monday at 4am UTC
```

See [Knowledge Sync](../knowledge-sync.md) for CLI commands and setup instructions.
