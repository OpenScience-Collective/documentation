# Tools

OSA provides a modular tool system for document retrieval, validation, and knowledge search. Tools are organized by domain and can be composed into assistant workflows.

## Modular Design

Each assistant in OSA has its own set of tools that can be independently developed and added. When a new assistant is added to OSA, its documentation is automatically populated here.

## Assistant Tool Sets

### HED Tools

Tools for working with Hierarchical Event Descriptors (HED).

- [HED Tools](hed.md) - Document retrieval, validation, tag suggestions

**Status:** Available

### BIDS Tools

Tools for working with Brain Imaging Data Structure (BIDS).

**Status:** Planned - will be added when BIDS assistant is implemented

### EEGLAB Tools

Tools for working with EEGLAB analysis toolbox.

**Status:** Planned - will be added when EEGLAB assistant is implemented

---

## Common Tool Categories

Each assistant typically provides tools in these categories:

### Document Retrieval

Fetch documentation from official sources:

| Tool Pattern | Description |
|--------------|-------------|
| `retrieve_{domain}_docs` | Fetch documentation by topic |

### Validation

Validate domain-specific data:

| Tool Pattern | Description |
|--------------|-------------|
| `validate_{domain}_*` | Validate domain data |
| `get_{domain}_schema_versions` | List schema versions |

### Knowledge Search

Search community knowledge:

| Tool Pattern | Description |
|--------------|-------------|
| `search_github_issues` | Search GitHub issues and PRs |
| `search_papers` | Search OpenALEX for academic papers |
| `search_discourse` | Search Neurostars and other forums |

## Tool Architecture

Tools follow a common pattern using LangChain:

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class RetrieveDocsInput(BaseModel):
    """Input for document retrieval."""
    topic: str = Field(description="Topic to search for")
    max_docs: int = Field(default=3, description="Maximum documents")

@tool(args_schema=RetrieveDocsInput)
def retrieve_docs(topic: str, max_docs: int = 3) -> str:
    """Retrieve documentation for a topic."""
    # Implementation
    pass
```

## Tool Permissions

Some tools require explicit user permission:

| Permission Level | Examples | Reason |
|------------------|----------|--------|
| None | `retrieve_*_docs`, `validate_*` | Read-only operations |
| Required | `create_github_issue` | Creates external resources |
| Required | `send_email` | External communication |

## Adding Custom Tools

Communities can add their own tools:

1. Create a tool function with `@tool` decorator
2. Add to the tool registry in `src/tools/`
3. Include in assistant configuration
4. Add documentation in `docs/osa/tools/{domain}.md`

See [Development](../development.md) for detailed instructions.
