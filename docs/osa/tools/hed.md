# HED Tools

The Hierarchical Event Descriptors (HED) assistant provides tools for document retrieval, knowledge search, string validation, schema version lookup, and tag suggestions.

## Overview

| Tool | Type | Description |
|------|------|-------------|
| `retrieve_hed_docs` | Document retrieval | Fetch HED documentation by topic |
| `search_hed_discussions` | Knowledge search | Search GitHub issues and PRs |
| `list_hed_recent` | Knowledge search | List recent GitHub activity |
| `search_hed_papers` | Knowledge search | Search academic papers |
| `validate_hed_string` | HED-specific | Validate HED annotation strings via hedtools.org API |
| `get_hed_schema_versions` | HED-specific | List available HED schema versions |
| `suggest_hed_tags` | HED-specific | Suggest HED tags from natural language via hed-lsp |

## Document Retrieval

### `retrieve_hed_docs`

Fetch HED documentation by topic from configured sources.

**Preloaded documents** (embedded in system prompt):

| Category | Document |
|----------|----------|
| Core | HED annotation semantics |
| Specification | HED terminology |
| Specification | Basic annotation |
| Introductory | Introduction to HED |
| Introductory | How can you use HED? |

**On-demand documents** (fetched via tool):

| Category | Examples |
|----------|----------|
| Specification | HED formats, Advanced annotation, Library schemas |
| Quickstart | HED annotation quickstart, BIDS quickstart, NWB quickstart |
| Tools | Python tools, MATLAB tools, JavaScript tools, Online tools |
| Advanced | Schema developers guide, Validation guide, Search guide |

## Knowledge Search Tools

These tools search the HED community's synced knowledge database.

### `search_hed_discussions`

Search GitHub issues and PRs across HED repositories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `include_issues` | `bool` | `True` | Include issues in results |
| `include_prs` | `bool` | `True` | Include pull requests |
| `limit` | `int` | `5` | Maximum results |

**Tracked repositories:**

- `hed-standard/hed-specification`
- `hed-standard/hed-schemas`
- `hed-standard/hed-javascript`
- `hed-standard/hed-python`

### `list_hed_recent`

List recent GitHub activity ordered by creation date.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `item_type` | `str` | `"all"` | Filter: `"all"`, `"issue"`, or `"pr"` |
| `repo` | `str \| None` | `None` | Filter by repository |
| `status` | `str \| None` | `None` | Filter: `"open"` or `"closed"` |
| `limit` | `int` | `10` | Maximum results |

### `search_hed_papers`

Search academic papers related to HED.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `5` | Maximum results |

## HED-Specific Tools

### `validate_hed_string`

Validate HED annotation strings using the hedtools.org API. The agent uses this to self-check examples before showing them to users.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hed_string` | `str` | required | HED string to validate (e.g., `"Onset, Sensory-event"`) |
| `schema_version` | `str` | `"8.4.0"` | Schema version to validate against |

**Returns:**

```json
{
  "valid": true,
  "errors": "",
  "schema_version": "8.4.0"
}
```

When validation fails, `errors` contains a string describing the issues:

```json
{
  "valid": false,
  "errors": "Tag 'Invalid-tag' not found in schema",
  "schema_version": "8.4.0"
}
```

If the hedtools.org API is unreachable, the tool returns an error message instructing the agent not to present unvalidated tags.

### `get_hed_schema_versions`

List available HED schema versions from hedtools.org.

**Returns:**

```json
{
  "versions": ["8.4.0", "8.3.0", "8.2.0", "8.1.0", "8.0.0"],
  "error": ""
}
```

### `suggest_hed_tags`

Get HED tag suggestions from natural language using hed-lsp semantic search.

**Prerequisites:** Requires the [hed-lsp](https://github.com/hed-standard/hed-lsp) CLI. The tool searches for it in this order:

1. `hed-suggest` in PATH (global install)
2. Path specified by the `HED_LSP_PATH` environment variable (`$HED_LSP_PATH/server/out/cli.js`)
3. Common local dev path (`~/Documents/git/HED/hed-lsp/server/out/cli.js`)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_terms` | `list[str]` | required | Natural language descriptions |
| `top_n` | `int` | `10` | Max suggestions per term |

**Returns:**

```json
{
  "button press": ["Button", "Response-button", "Mouse-button", "Press", "Push"],
  "visual flash": ["Flash", "Flickering", "Visual-presentation"]
}
```

If hed-lsp is unavailable, returns empty lists with an `"error"` key.

## External APIs

HED tools integrate with external services:

| Service | Endpoint | Purpose |
|---------|----------|---------|
| hedtools.org | `https://hedtools.org/hed` | String validation, schema versions |
| hed-lsp | Local CLI | Tag suggestions from natural language |
| GitHub REST API | `https://api.github.com` | Issue/PR sync for knowledge search |
| OpenALEX / Semantic Scholar / PubMed | Various | Academic paper sync |
