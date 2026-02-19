# Development

Guide for contributing to OSA development.

## Development Workflow

All development follows: **Issue -> Feature Branch -> PR -> Review -> Merge**

1. **Pick an issue** from GitHub Issues
2. **Create feature branch from develop**: `git checkout develop && git checkout -b feature/issue-N-short-description`
3. **Implement** with atomic commits
4. **Create PR to develop** with `gh pr create --base develop`
5. **Address review findings** before merging
6. **Squash merge** to keep history clean

```bash
# Example workflow
gh issue list                                    # Find issue to work on
git checkout develop && git pull                 # Start from develop
git checkout -b feature/issue-7-interfaces       # Create branch
# ... implement ...
git add -A && git commit -m "feat: add X"        # Atomic commits
gh pr create --base develop --title "feat: add X" --body "Closes #7"
git push -u origin feature/issue-7-interfaces
gh pr merge --squash --delete-branch             # Squash merge
```

## Setup

```bash
# Clone repository
git clone https://github.com/OpenScience-Collective/osa
cd osa

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Copy environment file
cp .env.example .env
# Edit .env with your API keys
```

## Testing

### Guidelines

- **NO MOCKS**: Real tests with real data only
- **Dynamic tests**: Query registries/configs, don't hardcode values
- **Coverage**: >70% minimum
- **LLM testing**: Use exemplar scenarios from real cases

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov

# Run LLM integration tests
uv run pytest -m llm

# Run specific test file
uv run pytest tests/test_hed_tools.py -v
```

## Code Style

### Tools

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check style
uv run ruff check .

# Fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Guidelines

- Type hints required for all public APIs
- Docstrings for public functions and classes (Google style)
- Atomic commits with concise messages, no emojis
- 100 character line length

## Project Structure

```
src/
├── api/                    # FastAPI backend
│   ├── main.py            # App entry point
│   ├── config.py          # Settings
│   └── security.py        # Authentication
├── cli/                    # Typer CLI
│   ├── main.py            # Commands
│   ├── client.py          # HTTP client
│   └── config.py          # User config
├── agents/                 # LangGraph agents
│   ├── state.py           # State definitions
│   └── base.py            # Base agent classes
├── core/services/          # Business logic
│   └── llm.py             # LLM abstraction
└── tools/                  # Tool implementations
    ├── hed_docs.py        # HED document retrieval
    ├── hed_validation.py  # HED validation
    └── document_retrieval.py  # Base retrieval
```

## Adding a New Tool

1. Create tool function with `@tool` decorator:

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Input schema for my tool."""
    param: str = Field(description="Parameter description")

@tool(args_schema=MyToolInput)
def my_tool(param: str) -> str:
    """Tool description shown to LLM."""
    # Implementation
    return result
```

2. Add to tool registry in assistant configuration

3. Write tests (with real data, no mocks)

## Adding a New Community Assistant

Adding a new research community to OSA is primarily a YAML configuration task. For the full walkthrough, see the [Community Registry](registry/index.md) documentation:

1. **[Adding a Community](registry/quick-start.md)** - Create `src/assistants/{community-id}/config.yaml` with documentation sources, GitHub repos, citations, and system prompt
2. **[Local Testing](registry/local-testing.md)** - Validate config, test endpoints, verify documentation retrieval, and sync knowledge
3. **[Schema Reference](registry/schema-reference.md)** - Full YAML schema documentation for all configuration fields
4. **[Extensions](registry/extensions.md)** - Add specialized Python tools (e.g., validation APIs, schema queries)

The registry auto-discovers any `config.yaml` placed under `src/assistants/*/` and creates API endpoints, CLI commands, and auto-generated tools automatically.

## Key Documentation

- `.context/plan.md` - Implementation roadmap
- `.context/research.md` - Technical notes
- `.rules/` - Development standards

## References

- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent orchestration
- [LangChain](https://python.langchain.com/) - LLM framework
- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Typer](https://typer.tiangolo.com/) - CLI framework
