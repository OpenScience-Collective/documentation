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

Interactive chat mode with a specific assistant.

```bash
# Start chat with HED assistant
uv run osa chat --assistant hed

# Start chat with BIDS assistant
uv run osa chat --assistant bids
```

Options:
- `--assistant, -a`: Select assistant (hed, bids, eeglab). Default: hed
- `--standalone, -s`: Run in standalone mode without external server (default)
- `--url, -u`: API URL (overrides standalone mode)

Features:
- Multi-turn conversation with context
- Rich formatted output
- Tool call visibility

### `osa ask`

Single query mode for quick questions to a specific assistant.

```bash
# Ask the HED assistant
uv run osa ask -a hed "How do I annotate a button press?"

# Ask the BIDS assistant
uv run osa ask -a bids "How should I organize my EEG dataset?"
```

Options:
- `--assistant, -a`: Select assistant (hed, bids, eeglab). Default: hed
- `--standalone, -s`: Run in standalone mode without external server (default)
- `--url, -u`: API URL (overrides standalone mode)

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
# Interactive chat with HED assistant
uv run osa chat -a hed

# Quick question to HED assistant
uv run osa ask -a hed "What is HED?"

# Start server in background
uv run osa serve &
```

### Different Assistants

```bash
# HED assistant - annotation questions
uv run osa ask -a hed "How do I annotate visual stimuli?"

# BIDS assistant - data organization questions
uv run osa ask -a bids "How should I organize my EEG dataset?"

# EEGLAB assistant - analysis questions
uv run osa ask -a eeglab "How do I filter my EEG data?"
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
