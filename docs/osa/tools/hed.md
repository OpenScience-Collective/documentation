# HED Tools

Tools for working with Hierarchical Event Descriptors (HED).

## Document Retrieval

### `retrieve_hed_docs`

Fetch HED documentation by topic.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | string | Topic to search for |
| `max_docs` | int | Maximum documents to return (default: 3) |

**Example:**

```python
from src.tools.hed_docs import retrieve_hed_docs

result = retrieve_hed_docs.invoke({
    "topic": "annotation quickstart",
    "max_docs": 2
})
```

### Document Registry

OSA maintains a registry of HED documentation sources:

**Preloaded Documents (embedded in system prompt):**

| Category | Document |
|----------|----------|
| Core | HED annotation semantics |
| Specification | HED terminology |
| Specification | Basic annotation |
| Introductory | Introduction to HED |
| Introductory | How can you use HED? |

**On-Demand Documents (fetched via tool):**

| Category | Examples |
|----------|----------|
| Specification | HED formats, Advanced annotation, Library schemas |
| Quickstart | HED annotation quickstart, BIDS quickstart, NWB quickstart |
| Tools | Python tools, MATLAB tools, JavaScript tools, Online tools |
| Advanced | Schema developers guide, Validation guide, Search guide |

## Validation

### `validate_hed_string`

Validate HED annotation strings using the hedtools.org API.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `hed_string` | string | HED string to validate |
| `schema_version` | string | Schema version (default: latest) |

**Example:**

```python
from src.tools.hed_validation import validate_hed_string

result = validate_hed_string.invoke({
    "hed_string": "Sensory-event, Visual-presentation",
    "schema_version": "8.4.0"
})

# Returns:
# {
#   "valid": true,
#   "errors": [],
#   "warnings": []
# }
```

### `get_hed_schema_versions`

List available HED schema versions.

**Example:**

```python
from src.tools.hed_validation import get_hed_schema_versions

versions = get_hed_schema_versions.invoke({})
# ['8.4.0', '8.3.0', '8.2.0', ...]
```

## Tag Suggestions

### `suggest_hed_tags`

Get HED tag suggestions from natural language using hed-lsp.

**Prerequisites:** Requires [hed-lsp](https://github.com/hed-standard/hed-lsp) to be installed.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search_terms` | list[str] | Natural language descriptions |
| `top_n` | int | Number of suggestions per term (default: 5) |

**Example:**

```python
from src.tools.hed_validation import suggest_hed_tags

result = suggest_hed_tags.invoke({
    'search_terms': ['button press', 'visual flash'],
    'top_n': 5
})

# Returns:
# {
#   'button press': ['Button', 'Response-button', 'Mouse-button', 'Press', 'Push'],
#   'visual flash': ['Flash', 'Flickering', 'Visual-presentation']
# }
```

**CLI Usage:**

```bash
hed-suggest "button press"
# Button, Response-button, Mouse-button, Press, Push

hed-suggest --json "button" "stimulus"
# {"button": [...], "stimulus": [...]}
```

## External APIs

HED tools integrate with external services:

| Service | Endpoint | Purpose |
|---------|----------|---------|
| hedtools.org | https://hedtools.org/hed | String, sidecar, spreadsheet validation |
| hed-lsp | Local CLI | Tag suggestions from natural language |
| GitHub | https://api.github.com | HED specification issues and PRs |
