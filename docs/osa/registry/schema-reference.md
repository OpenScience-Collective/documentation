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
| `cors_origins` | list[string] | No | `[]` | Allowed CORS origins for widget embedding |
| `openrouter_api_key_env_var` | string | No | Platform key | Env var name for community API key |
| `default_model` | string | No | Platform default | Default LLM model (OpenRouter format) |
| `default_model_provider` | string | No | OpenRouter default | Provider routing preference |
| `enable_page_context` | boolean | No | `true` | Enable page context tool for widget embedding |
| `maintainers` | list[string] | No | `[]` | Community maintainer GitHub usernames |
| `documentation` | list | No | `[]` | Documentation sources |
| `github` | object | No | `null` | GitHub sync configuration |
| `citations` | object | No | `null` | Paper/citation search config |
| `docstrings` | object | No | `null` | Code docstring extraction config |
| `mailman` | list | No | `[]` | Mailing list archive configs |
| `faq_generation` | object | No | `null` | LLM-based FAQ generation config |
| `sync` | object | No | `null` | Per-type cron sync schedules |
| `budget` | object | No | `null` | Per-community spending limits |
| `discourse` | list | No | `[]` | Discourse forum configs |
| `widget` | object | No | `null` | Widget display configuration (title, greeting, suggestions) |
| `extensions` | object | No | `null` | Extension points (plugins, MCP) |
| `links` | object | No | `null` | External links (homepage, documentation, repository, demo) |

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

## `cors_origins`

Allowed CORS origins for widget embedding. Required if you plan to embed the widget on your website.

- Must include scheme (`https://` or `http://`)
- Supports wildcard subdomains (`*.example.org`)
- No path, query, or fragment allowed
- Max 255 characters per origin

```yaml
cors_origins:
  # Production website
  - https://myproject.org
  - https://www.myproject.org

  # Development/preview environments
  - https://*.pages.dev           # Cloudflare Pages previews
  - https://*.vercel.app          # Vercel previews
  - http://localhost:3000         # Local development

  # Subdomain wildcard
  - https://*.myproject.org       # Matches docs.myproject.org, etc.
```

!!! tip "CORS Best Practices"
    - Only add origins you control
    - Use specific domains when possible
    - Wildcards only for preview environments
    - Never use `*` alone

## `openrouter_api_key_env_var`

Environment variable name containing your community's OpenRouter API key. This enables per-community cost attribution.

```yaml
openrouter_api_key_env_var: OPENROUTER_API_KEY_HED
```

Setup on the server:
```bash
export OPENROUTER_API_KEY_HED="sk-or-v1-your-api-key-here"
```

Without a community key, costs are billed to the platform's shared key with shared rate limits.

## `default_model`

Default LLM model in OpenRouter format (`creator/model-name`).

```yaml
# Cost-effective (recommended for most communities)
default_model: anthropic/claude-haiku-4.5

# Balanced capability and cost
default_model: anthropic/claude-sonnet-4.5

# Maximum capability (expensive)
default_model: anthropic/claude-opus-4.5
```

| Model | Cost (per 1M tokens) | Use Case |
|-------|---------------------|----------|
| Haiku | ~$0.25 | General Q&A |
| Sonnet | ~$3.00 | Complex tasks |
| Opus | ~$15.00 | Critical accuracy |

## `default_model_provider`

Provider routing preference for performance optimization.

```yaml
default_model: anthropic/claude-haiku-4.5
default_model_provider: Cerebras    # Route to Cerebras for speed
```

Common providers: `Cerebras` (ultra-fast), `Together` (balanced). Availability varies by model.

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

## `maintainers`

List of community maintainer GitHub usernames. Used for scoped admin access and budget alert notifications.

```yaml
maintainers:
  - username1
  - username2
```

## `docstrings`

Configuration for extracting code docstrings from GitHub repositories. Enables the `search_{community}_code_docs` tool.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `repos` | list | Yes | - | Repositories to extract docstrings from |

### DocstringRepoConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `repo` | string | Yes | - | Repository in `org/repo` format |
| `branch` | string | No | `main` | Branch to extract from |
| `languages` | list[string] | Yes | - | Languages to extract: `matlab`, `python` |

```yaml
docstrings:
  repos:
    - repo: sccn/eeglab
      branch: develop
      languages: [matlab, python]
    - repo: sccn/ICLabel
      branch: master
      languages: [matlab]
```

## `mailman`

List of Mailman mailing list archives to sync. Enables the mailing list sync and FAQ generation pipeline.

### MailmanConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `list_name` | string | Yes | - | Mailing list name (used in archive URL) |
| `base_url` | URL | Yes | - | Base URL of the Mailman pipermail archive |
| `display_name` | string | No | `null` | Human-readable name for the list |
| `start_year` | int | No | `null` | Earliest year to sync |

```yaml
mailman:
  - list_name: eeglablist
    base_url: https://sccn.ucsd.edu/pipermail/eeglablist/
    display_name: EEGLAB Mailing List
    start_year: 2004
```

## `faq_generation`

Configuration for the two-stage LLM pipeline that generates FAQ entries from mailing list threads. The pipeline first scores thread quality (cheap), then summarizes high-quality threads (quality).

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `evaluation_agent` | object | No | - | Model config for scoring thread quality |
| `summary_agent` | object | No | - | Model config for generating FAQ summaries |
| `quality_threshold` | float | No | `0.7` | Minimum quality score to create FAQ (0.0-1.0) |
| `sources` | object | No | - | Source-specific settings |

### Agent Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model` | string | Yes | - | Model in OpenRouter format |
| `provider` | string | No | - | Provider routing preference |
| `temperature` | float | No | `0.0` | LLM temperature |
| `enable_caching` | bool | No | `true` | Enable prompt caching |

```yaml
faq_generation:
  evaluation_agent:
    model: qwen/qwen3-235b-a22b-2507
    provider: DeepInfra/FP8
    temperature: 0.0
    enable_caching: true

  summary_agent:
    model: anthropic/claude-haiku-4.5
    provider: Anthropic
    temperature: 0.1
    enable_caching: true

  quality_threshold: 0.7

  sources:
    mailman:
      enabled: true
      min_messages: 2
      min_participants: 2
```

## `sync`

Per-community sync schedules. Each sync type can have its own cron expression (APScheduler format, UTC timezone).

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `github` | object | No | - | GitHub sync schedule |
| `papers` | object | No | - | Paper sync schedule |
| `docstrings` | object | No | - | Docstring sync schedule |
| `mailman` | object | No | - | Mailing list sync schedule |
| `faq` | object | No | - | FAQ generation schedule |
| `beps` | object | No | - | BEP sync schedule |

Each schedule object has a single `cron` field.

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

## `budget`

Per-community spending limits for cost management.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `daily_limit_usd` | float | No | - | Maximum daily spend in USD |
| `monthly_limit_usd` | float | No | - | Maximum monthly spend in USD |
| `alert_threshold_pct` | float | No | `80.0` | Alert when this percentage of budget is reached |

```yaml
budget:
  daily_limit_usd: 5.00
  monthly_limit_usd: 50.00
  alert_threshold_pct: 80.0
```

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

## `widget`

Widget display configuration for the embedded chat widget. These values provide defaults that the widget loads from the `/communities` API endpoint, so embedders only need to set `communityId` in their JavaScript.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | string | No | Community `name` | Widget header title (max 100 chars) |
| `initial_message` | string | No | `null` | Greeting message shown when chat opens (max 1000 chars) |
| `placeholder` | string | No | `"Ask a question..."` | Input field placeholder text (max 200 chars) |
| `suggested_questions` | list[string] | No | `[]` | Clickable suggestion buttons (max 10) |
| `theme_color` | string | No | `null` | Primary theme color as hex `#RRGGBB` (e.g., `#008a79`) |
| `logo_url` | string | No | `null` | URL for custom logo/icon image |

### `theme_color`

Primary color applied to the widget button, header background, and accent elements. Must be a 6-digit hex color code.

```yaml
widget:
  theme_color: "#008a79"    # Teal
```

When not set, the widget uses the platform default blue (`#2563eb`). The widget JS also accepts `themeColor` via `setConfig()` for per-page overrides.

### `logo_url`

URL to a custom logo or icon image displayed in the widget header avatar (replacing the default brain icon).

- Must use `http://`, `https://`, or start with `/` (relative path)
- Max 500 characters

```yaml
widget:
  logo_url: https://example.com/my-logo.png
```

**Convention-based detection**: If `logo_url` is not set in the YAML, the API automatically checks for a `logo.*` file in the community's folder (`src/assistants/{id}/`). Supported formats: SVG, PNG, JPG, JPEG, WEBP. SVG is preferred over other formats when multiple exist. The file is served via the `GET /{community_id}/logo` endpoint.

**Precedence** (highest to lowest):

1. Widget JS `setConfig({ logo: 'url' })` -- embedder override
2. YAML `widget.logo_url` -- community maintainer sets explicit URL
3. Convention file -- `logo.png` or `logo.svg` in `src/assistants/{id}/`
4. Default brain icon (built into the widget)

### Example

```yaml
widget:
  title: HED Assistant
  theme_color: "#1a365d"
  initial_message: "Hi! I'm the HED Assistant. I can help with HED annotation, validation, and related tools."
  placeholder: Ask about HED...
  suggested_questions:
    - What is HED and how is it used?
    - How do I annotate an event with HED tags?
    - What tools are available for working with HED?
    - Explain this HED validation error.
```

When the widget is embedded on a page, it fetches community defaults from `GET /communities` and applies them automatically. Embedders can still override any field via `setConfig()` in JavaScript; see the [Widget Deployment Guide](../deployment/widget.md).

If `widget` is omitted, the widget falls back to generic defaults (title = community name, placeholder = "Ask a question...", platform blue theme, brain icon).

## `enable_page_context`

When `true` (default), the assistant includes a `fetch_current_page` tool that retrieves content from the web page where the widget is embedded. This allows the assistant to provide contextually relevant answers based on what the user is currently reading.

Set to `false` if the assistant will only be used via CLI or API (not embedded in a web page).

## `links`

External links for the community, exposed via the `/communities` API endpoint. Only populated links are included in the response.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `homepage` | URL | No | `null` | Primary community website |
| `documentation` | URL | No | `null` | Documentation or tutorials URL |
| `repository` | URL | No | `null` | Source code repository (GitHub org or repo) |
| `demo` | URL | No | `null` | Live demo page URL |

```yaml
links:
  homepage: https://www.fieldtriptoolbox.org
  documentation: https://www.fieldtriptoolbox.org/tutorial/
  repository: https://github.com/fieldtrip/fieldtrip
  demo: https://demo.osc.earth/fieldtrip
```

All fields are optional. If no links are provided, the `links` field is omitted from the API response.

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

widget:
  title: HED Assistant
  theme_color: "#1a365d"
  initial_message: "Hi! I'm the HED Assistant. I can help with HED annotations."
  placeholder: Ask about HED...
  suggested_questions:
    - What is HED and how is it used?
    - How do I annotate an event with HED tags?

links:
  homepage: https://www.hedtags.org
  documentation: https://www.hed-resources.org
  repository: https://github.com/hed-standard

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
