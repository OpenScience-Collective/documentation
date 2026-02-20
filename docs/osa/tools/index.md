# Tools

OSA provides a modular tool system for document retrieval, validation, and knowledge search. Each community assistant gets its own set of tools, combining generic knowledge discovery tools with community-specific capabilities.

## Community Tool Sets

### HED Tools

Tools for working with Hierarchical Event Descriptors (HED).

- [HED Tools](hed.md) - Document retrieval, validation, tag suggestions, knowledge search

**Status:** Available

### BIDS Tools

Tools for working with Brain Imaging Data Structure (BIDS).

- [BIDS Tools](bids.md) - Document retrieval, BEP lookup, knowledge search

**Status:** Available

### EEGLAB Tools

Tools for working with the EEGLAB analysis toolbox.

- [EEGLAB Tools](eeglab.md) - Document retrieval, docstring search, FAQ search, knowledge search

**Status:** Available

### NEMAR Tools

Tools for discovering and exploring BIDS-formatted datasets from the NeuroElectroMagnetic Archive (NEMAR).

- [NEMAR Tools](nemar.md) - Dataset search and metadata retrieval

**Status:** Available

---

## Common Tool Categories

Every community assistant automatically receives knowledge discovery tools based on its YAML configuration. These are generated at startup by the `create_knowledge_tools` factory in `src/tools/knowledge.py`.

### Document Retrieval

Each community gets a `retrieve_{community}_docs` tool that fetches documentation from configured sources. Some docs are preloaded into the system prompt; the rest are fetched on demand.

| Tool Name | Description |
|-----------|-------------|
| `retrieve_{community}_docs` | Fetch documentation by topic from configured sources |

### Knowledge Search

Community-scoped tools for searching synced knowledge databases. All tools search the community's SQLite Full-Text Search 5 (FTS5) database at `data/knowledge/{community_id}.db`.

| Tool Name | Description | Requires |
|-----------|-------------|----------|
| `search_{community}_discussions` | Search GitHub issues and Pull Requests (PRs) | `github.repos` in config |
| `list_{community}_recent` | List recent GitHub activity by date | `github.repos` in config |
| `search_{community}_papers` | Search academic papers (OpenALEX, Semantic Scholar, PubMed) | `citations` in config |
| `search_{community}_code_docs` | Search code docstrings (MATLAB/Python) | `docstrings` in config |
| `search_{community}_faq` | Search mailing list FAQ entries | `mailman` + `faq_generation` in config |

### Validation

Some communities provide domain-specific validation tools:

| Tool Name | Description |
|-----------|-------------|
| `validate_{domain}_*` | Validate domain-specific data (e.g., HED strings) |

## Tool Architecture

Tools are built using LangChain's `@tool` decorator and `StructuredTool.from_function` factory:

```python
from langchain_core.tools import tool

@tool
def my_tool(query: str, limit: int = 5) -> str:
    """Tool description used by the agent."""
    # Implementation
    return "results"
```

Generic knowledge tools are created by factory functions in `src/tools/knowledge.py`. Community-specific tools are defined in `src/assistants/{community}/tools.py` and loaded as Python plugins via the `extensions.python_plugins` config.

## Tool Loading Order

When a community assistant starts, tools are loaded in this order:

1. **Knowledge tools** - `search_{community}_discussions`, `list_{community}_recent`, `search_{community}_papers`
2. **Conditional knowledge tools** - `search_{community}_code_docs` (if `docstrings` configured), `search_{community}_faq` (if `mailman` configured)
3. **Document retrieval** - `retrieve_{community}_docs`
4. **Page context** - `fetch_current_page` (if `enable_page_context: true`)
5. **Python plugin tools** - Custom tools from `extensions.python_plugins`

## Adding Custom Tools

Communities can add tools through the Python plugin system:

1. Create a tool module at `src/assistants/{community}/tools.py`
2. Define tools using the `@tool` decorator
3. Export them via `__all__`
4. Register in `config.yaml` under `extensions.python_plugins`

See [Extensions](../registry/extensions.md) for details.
