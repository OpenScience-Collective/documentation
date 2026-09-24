# OpenNeuroPET Tools

The OpenNeuroPET assistant provides tools for documentation retrieval and
GitHub knowledge search, covering the OpenNeuroPET ecosystem of open and
reproducible tools for Positron Emission Tomography (PET) imaging:
PET2BIDS (DICOM/ECAT to BIDS conversion), petprep (a BIDS App for
preprocessing), bloodstream (blood data analysis), petfit (kinetic
modeling), and PetSurfer.

## Overview

| Tool | Type | Description |
|------|------|--------------|
| `retrieve_openneuropet_docs` | Document retrieval | Fetch OpenNeuroPET, petprep, and petfit documentation |
| `search_openneuropet_discussions` | Knowledge search | Search GitHub issues and PRs |
| `list_openneuropet_recent` | Knowledge search | List recent GitHub activity |

OpenNeuroPET has no `citations`, `docstrings`, or `mailman` configuration,
so it does not get `search_openneuropet_papers`, `search_openneuropet_code_docs`,
or `search_openneuropet_faq`.

## Document Retrieval

### `retrieve_openneuropet_docs`

Fetches documentation from 23 configured sources across the OpenNeuroPET
tool ecosystem.

**Preloaded docs** (embedded in system prompt):

- Getting Started (overview of OpenNeuroPET tools)

**On-demand docs (22):** organized by tool:

- **petprep (6):** overview, installation, usage, workflows (motion
  correction, partial volume correction, spatial normalization), outputs,
  FAQ
- **petfit (14):** overview, installation, quick start, usage guide,
  region definition, plasma input modeling, reference tissue modeling,
  supported models, reports, outputs, folder structure, Docker usage,
  Apptainer usage, R API reference
- **PetSurfer (1):** wiki (partial volume correction and kinetic
  modeling using FreeSurfer)
- **BIDS (1):** the PET extension to the Brain Imaging Data Structure
  (BIDS) specification

## Knowledge Search Tools

These tools search the OpenNeuroPET community's synced knowledge database.

### `search_openneuropet_discussions`

Search GitHub issues and PRs across the OpenNeuroPET repositories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `include_issues` | `bool` | `True` | Include issues in results |
| `include_prs` | `bool` | `True` | Include pull requests |
| `limit` | `int` | `5` | Maximum results |

**Tracked repositories:**

- `openneuropet/openneuropet.github.io`
- `openneuropet/PET2BIDS`
- `nipreps/petprep`
- `mathesong/bloodstream`
- `mathesong/petfit`

### `list_openneuropet_recent`

List recent GitHub activity ordered by creation date.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `item_type` | `str` | `"all"` | Filter: `"all"`, `"issue"`, or `"pr"` |
| `repo` | `str \| None` | `None` | Filter by repository |
| `status` | `str \| None` | `None` | Filter: `"open"` or `"closed"` |
| `limit` | `int` | `10` | Maximum results |

## Sync Schedule

| Source | Schedule | Notes |
|--------|----------|-------|
| GitHub | Daily, 2:00 UTC | Issues and PRs from 5 repositories |

See [Knowledge Sync](../knowledge-sync.md) for CLI commands and setup instructions.
