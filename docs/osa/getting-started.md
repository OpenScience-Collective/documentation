# Getting Started

This guide will help you set up and start using the Open Science Assistant.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Git

## Installation

### Clone the Repository

```bash
git clone https://github.com/OpenScience-Collective/osa
cd osa
```

### Install Dependencies

```bash
# Install all dependencies
uv sync

# Install pre-commit hooks (for development)
uv run pre-commit install
```

### Configuration

OSA uses environment variables for configuration. Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# LLM Provider (OpenRouter recommended)
OPENROUTER_API_KEY=your-key-here

# Optional: LangFuse for observability
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com

# Optional: HED LSP for tag suggestions
HED_LSP_PATH=/path/to/hed-lsp
```

## Running OSA

### Development Server

```bash
# Start the FastAPI server
uv run uvicorn src.api.main:app --reload --port 38528
```

The API will be available at `http://localhost:38528`.

### CLI Usage

```bash
# Show available commands
uv run osa --help

# Interactive chat mode
uv run osa chat

# Single query
uv run osa ask "How do I validate a HED string?"

# Serve API (alternative to uvicorn)
uv run osa serve
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/info` | GET | API information |
| `/chat` | POST | Chat with streaming response |

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov

# Run LLM integration tests (requires API key)
uv run pytest -m llm
```

## Optional: HED Tag Suggestions

The HED assistant can suggest valid HED tags from natural language using the [hed-lsp](https://github.com/hed-standard/hed-lsp) CLI tool.

### Install hed-lsp

```bash
git clone https://github.com/hed-standard/hed-lsp.git
cd hed-lsp/server
npm install
npm run compile
```

### Configure

Set the `HED_LSP_PATH` environment variable:

```bash
export HED_LSP_PATH=/path/to/hed-lsp
```

Or install globally:

```bash
cd hed-lsp/server
npm link  # Makes hed-suggest available globally
```

### Usage

```python
from src.tools.hed_validation import suggest_hed_tags

result = suggest_hed_tags.invoke({
    'search_terms': ['button press', 'visual flash'],
    'top_n': 5
})
# {'button press': ['Button', 'Response-button', ...],
#  'visual flash': ['Flash', 'Flickering', ...]}
```

## Next Steps

- Read the [Architecture](architecture.md) documentation
- Explore [available tools](tools/index.md)
- Check the [CLI Reference](cli-reference.md)
