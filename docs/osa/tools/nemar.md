# NEMAR Tools

The NEMAR (NeuroElectroMagnetic Archive) assistant provides tools for
documentation retrieval and dataset discovery. NEMAR hosts hundreds of
Brain Imaging Data Structure (BIDS)-formatted EEG, MEG, and iEEG datasets
sourced from [OpenNeuro](https://openneuro.org/).

Dataset identifiers are `nm` or `on` followed by six digits, for example
`nm000103`. They are not OpenNeuro `ds` accessions.

## Overview

| Tool | Type | Description |
|------|------|-------------|
| `retrieve_nemar_docs` | Document retrieval | Fetch NEMAR, OpenNeuro, and BIDS reference documentation |
| `nemar_search_datasets` | Dataset discovery | Search or browse the public NEMAR dataset catalog |
| `nemar_describe_dataset` | Dataset discovery | Get a dataset's metadata, citation, and license |
| `nemar_list_recordings` | Dataset discovery | List a dataset's recordings and channel groups |
| `nemar_get_events` | Dataset discovery | Get one recording's BIDS events table |
| `nemar_render_overview` | Dataset discovery | Render a PNG overview image of one recording |
| `nemar_read_window` | Dataset discovery | Get a recipe (or a small decoded sample) for a time window |

## Document Retrieval

### `retrieve_nemar_docs`

Fetches documentation from three configured sources, none of them preloaded
into the system prompt:

- NEMAR dataset browser ([nemar.org/discover](https://nemar.org/discover))
- OpenNeuro platform ([openneuro.org](https://openneuro.org/))
- BIDS specification ([bids-specification.readthedocs.io](https://bids-specification.readthedocs.io/))

## Dataset Discovery Tools

These six tools come from NEMAR's own Model Context Protocol (MCP) server,
not from a `python_plugins` module. The community's `config.yaml` declares
it under `extensions.mcp_servers`:

```yaml
extensions:
  mcp_servers:
    - name: nemar
      url: https://mcp.nemar.org/mcp
```

OSA prefixes every tool the server advertises with the server's `name`, so
the MCP server's own `search_datasets` becomes `nemar_search_datasets` in
the assistant's tool list, and likewise for the other five. The server is
anonymous (no credentials needed) and stateless, so OSA opens a fresh
session per call rather than keeping one open.

They form a deliberate cost ladder, cheapest first; each step down reads
more of the underlying data, so the assistant is instructed to walk it
rather than jump to the bottom. `nemar_describe_dataset`'s response
includes a `cost_hint` naming the next cheapest tool for follow-up
questions about a specific dataset.

### `nemar_search_datasets`

Search or browse the public NEMAR dataset catalog. A free-text `query`
runs the exact-id, full-text, and semantic search tiers in that order;
every other parameter narrows the result set, and they compose.

**Common parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Free-text search over dataset name, description, authors, tasks, and modalities. Omit to browse the catalog instead. |
| `modality` | string | Substring match against recorded modalities (e.g. `"eeg"`, `"meg"`) |
| `task` | string | Substring match against task names |
| `has_hed` | boolean | Filter to datasets with Hierarchical Event Descriptors (HED) annotations |
| `has_zarr` | boolean | Filter to datasets with a converted Zarr serving copy |
| `author` | string | Substring match against author names |
| `has_doi` | boolean | Filter to datasets that carry a citable DOI |
| `license` | string | Comma-separated license tiers: `public`, `attribution`, `sharealike`, `noncommercial`, `noderiv`, `unknown` |
| `include_unknown` | boolean | Widen every active facet filter to also admit datasets whose value is unknown, rather than excluding them |
| `limit` | int | Maximum results to return (default 20, capped at 100) |

Beyond these, the tool accepts range-style facet filters over subject
count, channel count, session count, dataset size, file count, citation
count, recording duration, recording count, participant age, sampling
rate, power line frequency, electrode reference and placement, electrode
system, source archive, Zarr conversion status, BIDS version, and HED
version. This facet set is generated server-side and grows over time, so
it is read from the tool's own JSON schema at call time rather than
hand-copied here; passing a name the schema does not declare is accepted
and silently ignored, returning unfiltered results that look filtered.

A count of `0` is not an error: an unrecognized modality or task value
simply matches nothing.

### `nemar_describe_dataset`

Get a dataset's descriptive metadata: name, DOI, license, a ready-to-paste
citation string, modalities, tasks, subject count, HED and Zarr status,
plus a `cost_hint` naming the cheapest next tool to call. Never reads
`index.json` (the largest index in the catalog is 12.8 MB).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `dataset_id` | string | NEMAR dataset id: `nm` or `on` plus six digits, e.g. `nm000329` |

### `nemar_list_recordings`

List a converted dataset's recordings (Zarr stores) with their channel
groups. Parses `index.json` once per (dataset, source commit) and caches
the result, so repeat calls are cheap.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset_id` | string | required | NEMAR dataset id |
| `modality` | string | - | Case-insensitive filter against a group's modality |
| `min_duration_s` | number | - | Filter to recordings whose longest group duration is at least this many seconds |
| `include_derived` | boolean | `false` | Include Signal-Space Separation (SSS)-filtered derived stores |
| `limit` | int | `50` | Maximum recordings to return (capped at 500) |
| `offset` | int | `0` | Pagination offset |

A dataset that has not finished converting answers a typed tool error
naming its actual Zarr conversion status, never an empty list.

### `nemar_get_events`

Get one recording's BIDS events (onset, duration, trial type, value, HED,
sample index). Reads `events.parquet` when the dataset has one (exact
sample index); otherwise falls back to the recording's sibling
`events.tsv` and flags the result `estimated`.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset_id` | string | required | NEMAR dataset id |
| `recording` | string | required | A store's path or `zarr` field; either identifies the recording |
| `group` | string | - | Filter to one channel group's events by name |
| `limit` | int | `1000` | Maximum event rows to return (capped at 5000) |
| `offset` | int | `0` | Pagination offset |

### `nemar_render_overview`

Render a quick min-max envelope PNG image of one recording's channel
group, from the pre-computed view pyramid (never the level-0 array).
Cheap by construction: kilobytes read, one image returned, cached per
(dataset, source commit, recording, group, width).

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset_id` | string | required | NEMAR dataset id |
| `recording` | string | required | A store's path or `zarr` field |
| `group` | string | - | Which channel group to render; defaults to the first group |
| `width_px` | int | `800` | Rendered image width in pixels (capped at 4000) |

### `nemar_read_window`

Read a window of one recording's actual signal. By default (`taste:
false`) this returns a *recipe*: the array's coordinates plus a how-to
snippet per lane, with zero signal bytes touched. Pass `taste: true`
(and `channels`, then required) for a small, capped, inline-decoded
window of physical values instead: at most 60 seconds, 64 channels, and
65,536 channel-samples.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset_id` | string | required | NEMAR dataset id |
| `recording` | string | required | A store's path or `zarr` field |
| `group` | string | - | Which channel group to read; defaults to the first group |
| `start_s` | number | `0` | Window start, in seconds |
| `duration_s` | number | `10` | Window length in seconds (recipe mode up to 86400 s; a taste is additionally capped at 60 s) |
| `channels` | int[] | - | Channel indices; required when `taste` is true (capped at 4096, and additionally at 64 for a taste) |
| `taste` | boolean | `false` | `false` returns a read recipe; `true` decodes a small window inline |

The recipe names three read lanes that are not interchangeable:
`python_zarr` for desktop and HPC (`zarr` plus anonymous S3; not usable
in a browser), `python_browser` for Python running in a browser via
Pyodide, and `zarrita` for TypeScript/JavaScript in a browser or Node.

Needs a dataset converted to the v3 index format; a dataset still on
index format v1 answers a typed error (`nemar_list_recordings` and
`nemar_get_events` still work on it).

## Data Provenance

Every response from `nemar_list_recordings`, `nemar_get_events`,
`nemar_render_overview`, and `nemar_read_window` carries an `envelope`
with provenance the assistant is instructed to surface rather than
paper over:

- **`lossy` is always `true` today.** The streaming copy is quantized
  and rate-capped relative to the original recording; `effective_rate_hz`
  may be lower than `source_rate_hz`.
- **`zarr_verify_status` may be `null`**, meaning the standing fidelity
  sweep has not yet reached that conversion. That is "not checked," not
  "wrong."
- **`filled_ranges`** on a decoded `nemar_read_window` taste lists any
  sample spans that had no stored data and were filled in, rather than
  being real recorded signal.

## Related Links

- [NEMAR homepage](https://nemar.org)
- [NEMAR dataset browser](https://nemar.org/discover)
- [OpenNeuro](https://openneuro.org/) (source platform for all NEMAR datasets)
- [BIDS Specification](https://bids-specification.readthedocs.io/) (format standard for all NEMAR datasets)
