# CLI Reference

The OSA command-line interface provides quick access to the assistant.

## Installation

The CLI is included with OSA:

```bash
uv sync
uv run osa --help
```

## Commands

### `osa chat`

Interactive chat mode with the assistant.

```bash
uv run osa chat
```

Features:
- Multi-turn conversation
- Rich formatted output
- Streaming responses
- Tool call visibility

### `osa ask`

Single query mode for quick questions.

```bash
uv run osa ask "How do I annotate a button press in HED?"
```

Options:
- `--assistant`: Select assistant (hed, bids, eeglab)
- `--model`: Override default model

### `osa serve`

Start the API server.

```bash
uv run osa serve
```

Options:
- `--port`: Server port (default: 38528)
- `--host`: Host address (default: 127.0.0.1)
- `--reload`: Enable auto-reload for development

### `osa config`

Manage CLI configuration.

```bash
# Show current config
uv run osa config show

# Set a value
uv run osa config set api_url http://localhost:38528
```

Configuration is stored in `~/.config/osa/config.yaml`.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OSA_API_URL` | API server URL | `http://localhost:38528` |
| `OPENROUTER_API_KEY` | LLM provider API key | Required |
| `LANGFUSE_PUBLIC_KEY` | LangFuse public key | Optional |
| `LANGFUSE_SECRET_KEY` | LangFuse secret key | Optional |

### Config File

The CLI uses `~/.config/osa/config.yaml`:

```yaml
api_url: http://localhost:38528
default_assistant: hed
default_model: openai/gpt-4.1-mini
```

## Examples

### Basic Usage

```bash
# Interactive chat
uv run osa chat

# Quick question
uv run osa ask "What is HED?"

# Start server in background
uv run osa serve &
```

### With Specific Assistant

```bash
# Use HED assistant
uv run osa ask --assistant hed "How do I annotate visual stimuli?"

# Use BIDS assistant
uv run osa ask --assistant bids "How should I organize my EEG dataset?"
```

### Development

```bash
# Run with auto-reload
uv run osa serve --reload

# Run tests
uv run pytest tests/ -v

# Check coverage
uv run pytest --cov
```
