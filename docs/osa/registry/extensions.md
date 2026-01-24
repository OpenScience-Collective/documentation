# Extensions

Extensions add specialized tools to community assistants beyond what YAML can auto-generate. Use extensions when you need external API calls, CLI tool integration, or complex processing logic.

## When to Use Extensions

| Need | Solution |
|------|----------|
| Fetch documentation pages | Built-in (auto-generated from `documentation` config) |
| Search GitHub issues/PRs | Built-in (auto-generated from `github` config) |
| Search academic papers | Built-in (auto-generated from `citations` config) |
| Call an external validation API | **Python plugin** |
| Run a CLI tool | **Python plugin** |
| Connect to an MCP server | **MCP server extension** |

## Python Plugins

Python plugins are the primary extension mechanism. Each plugin is a Python module containing functions decorated with LangChain's `@tool`.

### Writing a Plugin

Create a `tools.py` file in your community directory:

```python
# src/assistants/my-tool/tools.py
"""Specialized tools for My Tool community."""

import httpx
from langchain_core.tools import tool


@tool
def validate_config(config_text: str, version: str = "2.0") -> dict:
    """Validate a My Tool configuration file.

    Args:
        config_text: The configuration content to validate.
        version: Schema version to validate against.

    Returns:
        Dict with 'valid' boolean and 'errors' list if invalid.
    """
    try:
        response = httpx.post(
            "https://my-tool.org/api/validate",
            json={"config": config_text, "version": version},
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"valid": False, "errors": [f"Validation service error: {e}"]}


@tool
def search_examples(query: str, limit: int = 5) -> list[dict]:
    """Search the My Tool examples database.

    Args:
        query: Search query describing the desired example.
        limit: Maximum number of results to return.

    Returns:
        List of matching examples with title, description, and code.
    """
    response = httpx.get(
        "https://my-tool.org/api/examples",
        params={"q": query, "limit": limit},
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json().get("results", [])
```

### Plugin Requirements

1. **Use `@tool` decorator** - This is the LangChain standard for tool definitions
2. **Clear docstring** - Becomes the tool description the LLM sees; be specific about what the tool does and when to use it
3. **Type hints** - All parameters must have type annotations
4. **Return JSON-serializable data** - Dicts, lists, strings, numbers, booleans
5. **Handle errors gracefully** - Return error information rather than raising exceptions

### Registering the Plugin

Reference your plugin module in `config.yaml`:

```yaml
extensions:
  python_plugins:
    - module: src.assistants.my-tool.tools
      tools:
        - validate_config
        - search_examples
```

If `tools` is omitted, all names exported in the module's `__all__` list that are valid tool objects are loaded:

```yaml
extensions:
  python_plugins:
    - module: src.assistants.my-tool.tools
      # All tools listed in __all__ are loaded
```

Your module must define `__all__` listing the tools to export:

```python
# src/assistants/my-tool/tools.py
__all__ = ["validate_config", "search_examples"]
```

### Example: HED Tools

The HED community has three specialized tools:

| Tool | Purpose | External Dependency |
|------|---------|---------------------|
| `validate_hed_string` | Validate HED annotations | hedtools.org REST API |
| `suggest_hed_tags` | Natural language to HED tags | hed-lsp CLI tool |
| `get_hed_schema_versions` | List available schema versions | hedtools.org REST API |

These tools call external APIs that provide domain-specific functionality (validation, tag suggestion) which cannot be replicated in YAML configuration alone.

### Best Practices

**Do:**

- Keep tools focused on a single task
- Return structured data the LLM can interpret
- Include usage guidance in the docstring (when to use, expected workflow)
- Handle network timeouts and errors
- Log errors for debugging (`logging.getLogger(__name__)`)

**Don't:**

- Create tools for documentation retrieval (use the `documentation` config instead)
- Include hardcoded secrets (use environment variables)
- Make tools that produce very long outputs (the LLM has limited context)
- Raise exceptions to the LLM (return error dicts instead)

### Tool Discovery

The `CommunityAssistant` loads plugin tools during initialization:

1. Imports the specified module
2. Filters for functions with the `@tool` decorator
3. If specific `tools` names are listed, only those are loaded
4. Tools are added to the LLM's tool list alongside auto-generated tools

## MCP Servers

MCP (Model Context Protocol) servers provide an alternative extension mechanism for tools that run as separate processes.

!!! note "Status"
    MCP server support is defined in the schema but not yet fully implemented in the runtime. The configuration is validated, and infrastructure is being built.

### Configuration

```yaml
extensions:
  mcp_servers:
    # Local server (started as a subprocess)
    - name: my-validator
      command: ["node", "path/to/mcp-server.js"]

    # Remote server (connects via URL)
    - name: remote-service
      url: https://mcp.my-tool.org
```

### Local vs Remote

| Type | Config | Use Case |
|------|--------|----------|
| Local | `command: [...]` | Tools bundled with your project |
| Remote | `url: https://...` | Shared services, heavy compute |

Exactly one of `command` or `url` must be provided for each server.

## Extension Loading Order

When a `CommunityAssistant` is created, tools are loaded in this order:

1. **Knowledge tools** from YAML config:
    - `list_{community}_recent` - Recent GitHub activity
    - `search_{community}_discussions` - GitHub search
    - `search_{community}_papers` - Academic paper search
2. **Documentation retrieval** - `retrieve_{community}_docs`
3. **Page context** - `fetch_current_page` (if `enable_page_context: true`)
4. **Additional tools** passed programmatically (if any)
5. **Python plugin tools** from `extensions.python_plugins`
6. **MCP server tools** from `extensions.mcp_servers` (when implemented)

All tools are available to the LLM simultaneously. The system prompt should guide the LLM on when to use each tool.
