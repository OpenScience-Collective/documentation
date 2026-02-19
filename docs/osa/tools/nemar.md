# NEMAR Tools

Tools for discovering and exploring BIDS-formatted EEG, MEG, and iEEG datasets from the NeuroElectroMagnetic Archive (NEMAR).

NEMAR hosts hundreds of BIDS-formatted neuroscience datasets sourced from [OpenNeuro](https://openneuro.org/), covering various experimental paradigms and recording modalities. These tools query the NEMAR public API to help researchers find datasets matching their research interests.

## Dataset Search

### `search_nemar_datasets`

Search NEMAR datasets with flexible text search and filtering. Fetches all datasets from the NEMAR API and filters client-side, returning compact summaries suitable for browsing.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | No | `null` | Text search across dataset names, tasks, README, and authors (case-insensitive substring match) |
| `modality_filter` | string | No | `null` | Filter by recording modality: `"EEG"`, `"MEG"`, `"iEEG"`, `"MRI"` (partial match, case-insensitive) |
| `task_filter` | string | No | `null` | Filter by experimental task name, e.g. `"rest"`, `"gonogo"`, `"memory"` (partial match, case-insensitive) |
| `has_hed` | boolean | No | `null` | If `true`, only return datasets with HED annotations |
| `min_participants` | int | No | `null` | Minimum number of participants required |
| `limit` | int | No | `20` | Maximum results to return (capped at 50) |

**Example:**

```python
from src.assistants.nemar.tools import search_nemar_datasets

# Find EEG datasets related to attention with at least 20 participants
result = search_nemar_datasets.invoke({
    "query": "attention",
    "modality_filter": "EEG",
    "min_participants": 20
})

# Find all datasets with HED annotations
result = search_nemar_datasets.invoke({
    "has_hed": True
})
```

**Returns:** Formatted markdown string with matching dataset summaries, each showing dataset ID, name, modalities, tasks, participant count, and size. When no matches are found, returns a message listing the active filters and total dataset count.

### `get_nemar_dataset_details`

Get comprehensive metadata for a specific NEMAR dataset, including description, citation, licensing, experimental details, and README content.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dataset_id` | string | Yes | - | Dataset identifier in the format `ds` followed by 4-6 digits (e.g. `"ds000248"`, `"ds005697"`) |

**Example:**

```python
from src.assistants.nemar.tools import get_nemar_dataset_details

result = get_nemar_dataset_details.invoke({
    "dataset_id": "ds000248"
})
```

**Returns:** Formatted markdown string with complete dataset information including:

- OpenNeuro and NEMAR links
- DOI and citation information
- Authors and license
- Data characteristics (modalities, tasks, participants, sessions, file count, size, age range)
- HED annotation status and version
- References, funding, acknowledgements
- README content (truncated to 1500 characters for long entries)

## Implementation Notes

- The NEMAR API has no server-side search capability, so `search_nemar_datasets` fetches all datasets (~485) and filters client-side
- Results are cached with a 5-minute TTL to avoid repeated API calls
- The API endpoint is `https://nemar.org/api/dataexplorer/datapipeline`
- Dataset IDs must match the pattern `ds` + 4-6 digits (validated before API calls)

## External APIs

| Service | Endpoint | Purpose |
|---------|----------|---------|
| NEMAR API | `https://nemar.org/api/dataexplorer/datapipeline/records` | Fetch all datasets for search |
| NEMAR API | `https://nemar.org/api/dataexplorer/datapipeline/datasetid` | Fetch single dataset details |

## Related Links

- [NEMAR homepage](https://nemar.org)
- [NEMAR Data Explorer](https://nemar.org/dataexplorer)
- [OpenNeuro](https://openneuro.org/) (source platform for all NEMAR datasets)
- [BIDS Specification](https://bids-specification.readthedocs.io/) (format standard for all NEMAR datasets)
