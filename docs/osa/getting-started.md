# Getting Started

This guide will help you set up and start using the Open Science Assistant.

## For Users (CLI)

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) or pip

### Install

```bash
pip install open-science-assistant
# or
uv pip install open-science-assistant
```

This installs a lightweight CLI (~7 dependencies) that connects to the OSA API.

### Setup

Run the interactive setup to configure your API key:

```bash
osa init
```

You'll need an [OpenRouter API key](https://openrouter.ai/keys). The setup will:

1. Prompt for your API key
2. Save it securely to `~/.config/osa/credentials.yaml` (permissions 600)
3. Test the connection to the API

Alternatively, pass the key directly:

```bash
osa init --api-key sk-or-v1-your-key
```

### Usage

```bash
# Ask a single question
osa ask -a hed "How do I annotate a button press?"

# Interactive chat session
osa chat -a hed

# Check API health
osa health

# See all commands
osa --help
```

You can also pass an API key per-command without saving it:

```bash
osa ask -a hed "What is HED?" --api-key sk-or-v1-your-key
```

Or set it via environment variable:

```bash
export OPENROUTER_API_KEY=sk-or-v1-your-key
osa ask -a hed "What is HED?"
```

## For Developers (Server)

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Clone and Install

```bash
git clone https://github.com/OpenScience-Collective/osa
cd osa

# Install all dependencies (including server + dev)
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Configuration

Copy the example environment file:

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
```

### Running the Server

```bash
# Start the FastAPI server
uv run uvicorn src.api.main:app --reload --port 38528

# Or use the CLI
uv run osa serve
```

The API will be available at `http://localhost:38528`.

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov

# Run LLM integration tests (requires API key)
uv run pytest -m llm
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/communities` | GET | List available communities |
| `/{community}/ask` | POST | Single question |
| `/{community}/chat` | POST | Multi-turn chat |

## Next Steps

- Read the [Architecture](architecture.md) documentation
- Explore [available tools](tools/index.md)
- Check the [CLI Reference](cli-reference.md)
