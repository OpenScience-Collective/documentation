# CLI Reference

The OSA command-line interface is a lightweight HTTP client that connects to the OSA API. It installs with minimal dependencies (~7 packages) and forwards your API key via BYOK headers.

## Installation

```bash
pip install open-science-assistant
# or
uv pip install open-science-assistant
```

To install server dependencies (for running the API server locally):

```bash
pip install 'open-science-assistant[server]'
```

## Commands

### `osa init`

Interactive setup to configure your API key and preferences.

```bash
# Interactive setup (prompts for API key)
osa init

# Non-interactive setup
osa init --api-key sk-or-v1-your-key

# With custom API URL
osa init --api-key sk-or-v1-your-key --api-url https://custom-server.example.com
```

Options:

- `--api-key, -k`: OpenRouter API key
- `--api-url`: Override API URL

### `osa ask`

Single query mode for quick questions.

```bash
# Ask the HED assistant
osa ask -a hed "How do I annotate a button press?"

# Ask the BIDS assistant
osa ask -a bids "How should I organize my EEG dataset?"

# JSON output (for scripting)
osa ask -a hed "What is HED?" -o json

# Disable streaming
osa ask -a hed "What is HED?" --no-stream
```

Options:

- `--assistant, -a`: Community assistant ID (hed, bids, eeglab). Default: hed
- `--api-key, -k`: OpenRouter API key (overrides saved config)
- `--api-url`: Override API URL
- `--output, -o`: Output format: rich, json, plain. Default: rich
- `--no-stream`: Disable streaming (get full response at once)

### `osa chat`

Interactive chat mode with conversation history.

```bash
# Start chat with HED assistant
osa chat -a hed

# Start chat with BIDS assistant
osa chat -a bids

# Disable streaming
osa chat -a eeglab --no-stream
```

Options:

- `--assistant, -a`: Community assistant ID (hed, bids, eeglab). Default: hed
- `--api-key, -k`: OpenRouter API key (overrides saved config)
- `--api-url`: Override API URL
- `--no-stream`: Disable streaming

Features:

- Multi-turn conversation with context
- Rich formatted output with Markdown rendering
- Tool call visibility
- Type 'quit', 'exit', or 'q' to end the session

### `osa health`

Check API health status.

```bash
# Check default API
osa health

# Check specific URL
osa health --url https://api.osc.earth/osa-dev
```

Options:

- `--url, -u`: API URL to check

### `osa version`

Show the installed OSA version.

```bash
osa version
```

### `osa config`

Manage CLI configuration.

#### `osa config show`

Display current configuration and credentials (masked).

```bash
osa config show
```

#### `osa config set`

Update configuration settings.

```bash
# Set API URL
osa config set --api-url https://custom-server.example.com

# Set OpenRouter API key
osa config set --openrouter-key sk-or-v1-your-key

# Set output format
osa config set --output json

# Enable/disable streaming
osa config set --no-streaming
```

Options:

- `--api-url`: API URL
- `--openrouter-key`: OpenRouter API key
- `--output, -o`: Output format (rich, json, plain)
- `--verbose/--no-verbose, -v`: Enable/disable verbose output
- `--streaming/--no-streaming`: Enable/disable streaming

#### `osa config path`

Show configuration and data directory paths.

```bash
osa config path
```

#### `osa config reset`

Reset configuration to defaults.

```bash
# With confirmation prompt
osa config reset

# Skip confirmation
osa config reset --yes
```

### `osa serve`

Start the OSA API server. Requires server dependencies.

```bash
# Install server dependencies first
pip install 'open-science-assistant[server]'

# Start server
osa serve

# Custom port and host
osa serve --port 8080 --host 0.0.0.0

# With auto-reload for development
osa serve --reload
```

Options:

- `--host, -h`: Host to bind to. Default: 0.0.0.0
- `--port, -p`: Port to bind to. Default: 38528
- `--reload, -r`: Enable auto-reload

### `osa sync`

Sync knowledge sources (GitHub issues/PRs, academic papers). Requires server dependencies.
See [Knowledge Sync](knowledge-sync.md) for details.

```bash
# Initialize database
osa sync init

# Sync GitHub issues/PRs
osa sync github

# Sync academic papers
osa sync papers

# Sync everything
osa sync all

# Check status
osa sync status
```

## Configuration

### API Key Priority

The CLI resolves API keys in this order:

1. `--api-key` command-line flag (highest priority)
2. `OPENROUTER_API_KEY` environment variable
3. Saved credentials in `~/.config/osa/credentials.yaml`

### Config Files

The CLI stores configuration in the platform-specific config directory:

| Platform | Path |
|----------|------|
| Linux | `~/.config/osa/` |
| macOS | `~/Library/Application Support/osa/` |
| Windows | `%APPDATA%\osa\` |

Files:

- `config.yaml`: Non-sensitive settings (API URL, output format)
- `credentials.yaml`: API keys (stored with restricted permissions, chmod 600)

Example `config.yaml`:

```yaml
api:
  url: https://api.osc.earth/osa
output:
  format: rich
  verbose: false
  streaming: true
```

### Environment Variables (CLI)

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | None |

### Environment Variables (Server)

These are only relevant when running the server (`osa serve`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Server-side LLM API key | Required |
| `LANGFUSE_PUBLIC_KEY` | LangFuse public key | Optional |
| `LANGFUSE_SECRET_KEY` | LangFuse secret key | Optional |
| `SYNC_ENABLED` | Enable automated knowledge sync | `true` |
| `SYNC_GITHUB_CRON` | GitHub sync schedule (cron) | `0 2 * * *` |
| `SYNC_PAPERS_CRON` | Papers sync schedule (cron) | `0 3 * * 0` |
| `GITHUB_TOKEN` | GitHub token for sync | Optional |
| `DATA_DIR` | Data directory for knowledge DB | Platform-specific |

## Examples

### Quick Start

```bash
# Install and setup
pip install open-science-assistant
osa init

# Ask a question
osa ask -a hed "What is HED?"
```

### Different Assistants

```bash
# HED assistant - annotation questions
osa ask -a hed "How do I annotate visual stimuli?"

# BIDS assistant - data organization questions
osa ask -a bids "How should I organize my EEG dataset?"

# EEGLAB assistant - analysis questions
osa ask -a eeglab "How do I filter my EEG data?"
```

### Scripting with JSON Output

```bash
# Get structured output
osa ask -a hed "What does HED stand for?" -o json

# Pipe to jq
osa ask -a hed "What is HED?" -o json | jq '.answer'
```

### Using with Environment Variable

```bash
export OPENROUTER_API_KEY=sk-or-v1-your-key
osa ask -a hed "What is HED?"
osa chat -a bids
```
