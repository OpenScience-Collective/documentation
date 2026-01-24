# YAML Schema Reference

Complete reference for the community `config.yaml` file format.

## Top-Level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | - | Unique identifier (kebab-case: `[a-z0-9]+(-[a-z0-9]+)*`) |
| `name` | string | Yes | - | Display name |
| `description` | string | Yes | - | Short description of the community/tool |
| `status` | enum | No | `available` | One of: `available`, `beta`, `coming_soon` |
| `system_prompt` | string | No | Built-in default | Custom system prompt template |
| `enable_page_context` | boolean | No | `true` | Enable page context tool for widget embedding |
| `documentation` | list | No | `[]` | Documentation sources |
| `github` | object | No | `null` | GitHub sync configuration |
| `citations` | object | No | `null` | Paper/citation search config |
| `discourse` | list | No | `[]` | Discourse forum configs |
| `extensions` | object | No | `null` | Extension points (plugins, MCP) |

## `id`

The community identifier used for API routing, storage, and CLI commands.

- Must be kebab-case: lowercase letters, numbers, and hyphens
- No leading or trailing hyphens
- Examples: `hed`, `bids`, `eeg-lab`, `my-tool-v2`

```yaml
id: hed          # Valid
id: my-tool      # Valid
id: MyTool       # Invalid - uppercase
id: my_tool      # Invalid - underscore
id: -my-tool     # Invalid - leading hyphen
```

## `system_prompt`

Template string for the LLM system prompt. Supports placeholders that are substituted at runtime:

| Placeholder | Substitution |
|-------------|--------------|
| `{name}` | Community display name |
| `{description}` | Community description |
| `{repo_list}` | Formatted list of GitHub repos (from `github.repos`) |
| `{paper_dois}` | Formatted list of tracked DOIs (from `citations.dois`) |
| `{preloaded_docs_section}` | Content of preloaded documents |
| `{available_docs_section}` | List of on-demand documents available via tool |
| `{page_context_section}` | Page context instructions (if `enable_page_context: true`) |
| `{additional_instructions}` | Extra instructions passed at creation time |

```yaml
system_prompt: |
  You are a technical assistant for {name}.
  {description}

  {preloaded_docs_section}

  {available_docs_section}

  {page_context_section}
```

If omitted, a built-in default prompt is used that includes the community name, description, and standard tool usage instructions.

## `documentation`

List of documentation sources. Each entry creates a retrievable document.

### DocSource Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | string | Yes | - | Human-readable title |
| `url` | URL | Yes | - | HTML page URL (shown to users in responses) |
| `source_url` | string | No | `null` | Raw content URL for fetching (required if `preload: true`) |
| `preload` | boolean | No | `false` | Embed in system prompt at startup |
| `category` | string | No | `general` | Category for organization |
| `type` | enum | No | `html` | Format: `sphinx`, `mkdocs`, `html`, `markdown`, `json` |
| `source_repo` | string | No | `null` | GitHub repo for raw markdown sources (e.g., 'org/repo') |
| `description` | string | No | `null` | Short description of document content |

### Preloaded vs On-Demand

**Preloaded** (`preload: true`): Content is fetched at startup and embedded directly in the system prompt. Use for core documentation the assistant always needs (2-3 docs max, keep total under 15k tokens).

**On-demand** (`preload: false` or omitted): Available via the auto-generated `retrieve_docs` tool. The assistant fetches these when relevant to the user's question.

```yaml
documentation:
  # Preloaded - always in context
  - title: Core Concepts
    url: https://my-tool.org/docs/concepts
    source_url: https://raw.githubusercontent.com/org/repo/main/docs/concepts.md
    preload: true
    category: core
    description: Fundamental concepts and terminology

  # On-demand - fetched when needed
  - title: Advanced Features
    url: https://my-tool.org/docs/advanced
    source_url: https://raw.githubusercontent.com/org/repo/main/docs/advanced.md
    category: advanced
    description: Advanced usage patterns and configuration
```

!!! warning "Preload Requirement"
    Documents with `preload: true` **must** have a `source_url` for fetching raw content. Validation will fail otherwise.

## `github`

GitHub repository configuration for syncing issues, pull requests, and discussions into the knowledge database.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `repos` | list[string] | No | `[]` | Repos in `org/repo` format |

```yaml
github:
  repos:
    - hed-standard/hed-specification
    - hed-standard/hed-python
    - hed-standard/hed-javascript
```

Repos are validated to match the `org/repo` format and deduplicated automatically.

## `citations`

Paper search and citation tracking configuration for the knowledge database.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `queries` | list[string] | No | `[]` | Search queries for OpenALEX |
| `dois` | list[string] | No | `[]` | Core paper DOIs to track (format: `10.xxxx/yyyy`) |

```yaml
citations:
  queries:
    - "HED annotation"
    - "Hierarchical Event Descriptors"
  dois:
    - "10.1016/j.neuroimage.2021.118766"
    - "10.1007/s12021-023-09628-4"
```

DOIs are validated against the `10.xxxx/yyyy` pattern. Common URL prefixes (`https://doi.org/`, `https://dx.doi.org/`) are automatically stripped.

## `discourse`

Discourse forum configurations for community Q&A search.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `url` | URL | Yes | - | Base URL of Discourse instance |
| `tags` | list[string] | No | `[]` | Tags to filter topics by |

```yaml
discourse:
  - url: https://neurostars.org
    tags:
      - hed
      - bids
```

## `extensions`

Extension points for specialized tools that cannot be auto-generated from YAML.

### Python Plugins

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `module` | string | Yes | - | Python module path |
| `tools` | list[string] | No | `null` | Specific tools to import (null = all) |

```yaml
extensions:
  python_plugins:
    - module: src.assistants.hed.tools
      tools:
        - validate_hed_string
        - suggest_hed_tags
        - get_hed_schema_versions
```

See [Extensions](extensions.md) for how to write Python plugin tools.

### MCP Servers

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | - | Server identifier |
| `command` | list[string] | No | `null` | Command for local server |
| `url` | URL | No | `null` | URL for remote server |

Exactly one of `command` or `url` must be provided.

```yaml
extensions:
  mcp_servers:
    - name: my-validator
      command: ["node", "path/to/server.js"]
    - name: remote-service
      url: https://mcp.my-tool.org
```

## `enable_page_context`

When `true` (default), the assistant includes a `fetch_current_page` tool that retrieves content from the web page where the widget is embedded. This allows the assistant to provide contextually relevant answers based on what the user is currently reading.

Set to `false` if the assistant will only be used via CLI or API (not embedded in a web page).

## Complete Example

```yaml
id: hed
name: HED (Hierarchical Event Descriptors)
description: Event annotation standard for neuroimaging research
status: available

enable_page_context: true

system_prompt: |
  You are a technical assistant specialized in HED.
  ...
  {preloaded_docs_section}
  {available_docs_section}
  {page_context_section}

documentation:
  - title: HED annotation semantics
    url: https://www.hedtags.org/hed-resources/HedAnnotationSemantics.html
    source_url: https://raw.githubusercontent.com/.../HedAnnotationSemantics.md
    preload: true
    category: core
    description: Fundamental annotation rules

  - title: Basic annotation
    url: https://www.hedtags.org/hed-specification/04_Basic_annotation.html
    source_url: https://raw.githubusercontent.com/.../04_Basic_annotation.md
    category: specification
    description: Essential guidelines for creating annotations

github:
  repos:
    - hed-standard/hed-specification
    - hed-standard/hed-python

citations:
  queries:
    - HED annotation
    - Hierarchical Event Descriptors
  dois:
    - "10.1016/j.neuroimage.2021.118766"

discourse:
  - url: https://neurostars.org
    tags:
      - hed

extensions:
  python_plugins:
    - module: src.assistants.hed.tools
      tools:
        - validate_hed_string
        - suggest_hed_tags
        - get_hed_schema_versions
```

## Validation

The configuration is validated using Pydantic models. Common validation errors:

| Error | Cause | Fix |
|-------|-------|-----|
| `Community ID must be kebab-case` | Uppercase or underscore in ID | Use lowercase with hyphens |
| `DocSource has preload=True but no source_url` | Missing fetch URL | Add `source_url` field |
| `Repository must be in 'org/repo' format` | Invalid repo format | Use `organization/repository` |
| `Invalid DOI format` | Malformed DOI | Use `10.xxxx/yyyy` format |
| `McpServer must have either 'command' or 'url'` | Missing server address | Add one of the fields |
| `extra fields not permitted` | Typo or unknown field | Check field names |

The `extra="forbid"` setting on all models means typos in field names will be caught as validation errors rather than silently ignored.
