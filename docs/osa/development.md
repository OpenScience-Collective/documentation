# Development

Guide for contributing to OSA development.

## Development Workflow

All development follows: **Issue -> Feature Branch -> PR -> Review -> Merge**

1. **Pick an issue** from GitHub Issues
2. **Create feature branch**: `git checkout -b feature/issue-N-short-description`
3. **Implement** with atomic commits
4. **Create PR** with `gh pr create`
5. **Address review findings** before merging
6. **Merge with merge commit** (never squash)

```bash
# Example workflow
gh issue list                                    # Find issue to work on
git checkout -b feature/issue-7-interfaces       # Create branch
# ... implement ...
git add -A && git commit -m "feat: add X"        # Atomic commits
gh pr create --title "feat: add X" --body "Closes #7"
git push -u origin feature/issue-7-interfaces
gh pr merge --merge --delete-branch              # Merge commit, never squash
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

## Adding a New Assistant

1. Create system prompt in `src/assistants/{name}/`
2. Configure tool set
3. Add routing rules in router agent
4. Write integration tests

## Key Documentation

- `.context/plan.md` - Implementation roadmap
- `.context/research.md` - Technical notes
- `.rules/` - Development standards

## References

- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent orchestration
- [LangChain](https://python.langchain.com/) - LLM framework
- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Typer](https://typer.tiangolo.com/) - CLI framework
