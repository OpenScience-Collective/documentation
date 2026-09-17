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

You'll need your own API key.
Either provider works:

- **Anthropic** (recommended): [platform.claude.com/settings/keys](https://platform.claude.com/settings/keys).
  Keys start with `sk-ant-`.
- **OpenRouter**: [openrouter.ai/keys](https://openrouter.ai/keys).
  Keys start with `sk-or-`.

The setup will:

1. Prompt for your API key
2. Work out which provider it belongs to from the key's own prefix, so there is nothing to declare
3. Save it securely to your config directory (see paths below)
4. Test the connection to the API

Config directory by platform:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/osa/` |
| Linux | `~/.config/osa/` |
| Windows | `%APPDATA%\osa\` |

Alternatively, pass the key directly:

```bash
osa init --api-key sk-ant-your-key
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
osa ask -a hed "What is HED?" --api-key sk-ant-your-key
```

Or set it via environment variable.
Each provider has its own variable, `ANTHROPIC_API_KEY` or `OPENROUTER_API_KEY`:

=== "macOS"

    ```bash
    export ANTHROPIC_API_KEY=sk-ant-your-key
    osa ask -a hed "What is HED?"
    ```

=== "Linux"

    ```bash
    export ANTHROPIC_API_KEY=sk-ant-your-key
    osa ask -a hed "What is HED?"
    ```

=== "Windows"

    ```powershell
    $env:ANTHROPIC_API_KEY = "sk-ant-your-key"
    osa ask -a hed "What is HED?"
    ```

!!! warning "One key at a time"

    If both variables are exported, the Anthropic key wins.
    A key passed with `--api-key` overrides both, and its provider is read from its prefix,
    so a typed OpenRouter key is not silently overridden by an exported `ANTHROPIC_API_KEY`.

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

=== "macOS"

    ```bash
    cp .env.example .env
    ```

=== "Linux"

    ```bash
    cp .env.example .env
    ```

=== "Windows"

    ```powershell
    Copy-Item .env.example .env
    ```

Edit `.env` with your settings:

```bash
# LLM provider: Claude Platform on AWS
ANTHROPIC_API_KEY=your-key-here
ANTHROPIC_BASE_URL=https://aws-external-anthropic.us-east-2.api.aws
ANTHROPIC_WORKSPACE_ID=wrkspc_your-workspace-id

# One of claude-haiku-4-5 (default) or claude-sonnet-5
DEFAULT_MODEL=claude-haiku-4-5

# Optional: LangFuse for observability
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

`ANTHROPIC_BASE_URL` and `ANTHROPIC_WORKSPACE_ID` go together:
the AWS endpoint requires an `anthropic-workspace-id` header,
so setting the base URL without the workspace id fails at request time.
Leave both unset to talk to `api.anthropic.com` with a first-party key instead.

!!! note "This is not Amazon Bedrock"

    The Claude Platform on AWS is Anthropic's own Messages API,
    billed through AWS Marketplace.
    It takes an `ANTHROPIC_API_KEY`, not AWS credentials,
    and OSA does not use the Bedrock SDK or Bedrock model identifiers.

`OPENROUTER_API_KEY` is still read, but only as a bring-your-own-key path;
it is never the platform default.
See [`.env.example`](https://github.com/OpenScience-Collective/osa/blob/main/.env.example)
for every variable with its own notes.

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

# Run LLM integration tests (real paid calls; needs ANTHROPIC_API_KEY)
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
