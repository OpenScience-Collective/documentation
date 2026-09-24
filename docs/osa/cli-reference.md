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
osa init --api-key sk-ant-your-key

# With custom API URL
osa init --api-key sk-ant-your-key --api-url https://custom-server.example.com
```

Options:

- `--api-key, -k`: Anthropic (`sk-ant-...`) or OpenRouter (`sk-or-...`) API key
- `--api-url`: Override API URL

Which provider the key belongs to is read from the key itself, so there is
nothing to choose. Get an Anthropic key at
[platform.claude.com/settings/keys](https://platform.claude.com/settings/keys),
or an OpenRouter key at [openrouter.ai/keys](https://openrouter.ai/keys).

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

- `--assistant, -a`: A community id, for example `hed` (see [Tools](tools/index.md) for the full list). Default: hed
- `--mirror, -m`: Mirror ID for ephemeral database routing (see [Database Mirrors](mirrors.md))
- `--api-key, -k`: Anthropic or OpenRouter API key (overrides saved config, and wins over both env vars)
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

- `--assistant, -a`: A community id, for example `hed` (see [Tools](tools/index.md) for the full list). Default: hed
- `--mirror, -m`: Mirror ID for ephemeral database routing (see [Database Mirrors](mirrors.md))
- `--api-key, -k`: Anthropic or OpenRouter API key (overrides saved config, and wins over both env vars)
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

# Set the Claude Platform key
osa config set --anthropic-key sk-ant-your-key

# Set an OpenRouter key instead, or as well
osa config set --openrouter-key sk-or-v1-your-key

# Set output format
osa config set --output json

# Enable/disable streaming
osa config set --no-streaming
```

Options:

- `--api-url`: API URL
- `--anthropic-key`: Anthropic API key
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

### `osa validate`

Validate a community configuration file. Requires server dependencies.

```bash
# File mode: YAML syntax, schema validation, env var checks
osa validate src/assistants/my-tool/config.yaml

# Also test the community's own API key against its provider
osa validate src/assistants/my-tool/config.yaml --test-api-key

# Community mode: full test suite, including URL accessibility and
# GitHub repo validation
osa validate --community hed

# Verbose pytest output in community mode
osa validate --community hed --verbose
```

Options:

- `config_path` (argument): path to a community's `config.yaml` (file mode; mutually exclusive with `--community`)
- `--community, -c`: community ID to validate with the full test suite instead of a single file
- `--test-api-key`: test the community's own API key against its provider (Anthropic or OpenRouter)
- `--verbose, -v`: show verbose pytest output when using `--community`

Exit code is 0 on success, 1 on failure.

### `osa mirror`

Manage ephemeral database mirrors for development. See [Database Mirrors](mirrors.md) for full documentation.

```bash
# Create a mirror
osa mirror create -c hed -c bids --label "my-test"

# List active mirrors
osa mirror list

# Show mirror details
osa mirror info abc123def456

# Delete a mirror
osa mirror delete abc123def456

# Re-copy production data into mirror
osa mirror refresh abc123def456

# Run sync pipeline against mirror
osa mirror sync abc123def456 --type github

# Download mirror databases locally
osa mirror pull abc123def456
```

### `osa sync`

Sync knowledge sources for community assistants. Requires server dependencies. All subcommands accept `--community/-c` to specify the target community.

See [Knowledge Sync](knowledge-sync.md) for full documentation.

```bash
# Initialize database for a community
osa sync init --community hed

# Sync GitHub issues/PRs
osa sync github --community bids

# Sync academic papers (with citation tracking)
osa sync papers --community bids

# Sync code docstrings (MATLAB/Python)
osa sync docstrings --community eeglab --language matlab

# Sync mailing list archives
osa sync mailman --community eeglab

# Generate FAQ from mailing list threads
osa sync faq --community eeglab --estimate

# Sync BIDS Extension Proposals
osa sync beps --community bids

# Sync everything for all communities
osa sync all

# Check status
osa sync status

# Search knowledge database
osa sync search "validation error" --community hed
```

## Configuration

### API Key Priority

The CLI carries one key per provider, and `-k/--api-key` selects its provider
from the key's own prefix.

1. `--api-key` command-line flag: wins outright, and leaves the other provider
   unset for that invocation, so an exported `ANTHROPIC_API_KEY` cannot
   override an OpenRouter key you just typed
2. `ANTHROPIC_API_KEY` or `OPENROUTER_API_KEY` environment variable
3. Saved credentials in `~/.config/osa/credentials.yaml`

With no flag, each provider resolves independently through steps 2 and 3.
When both end up set, Anthropic is used: it is the platform's own provider.

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
| `ANTHROPIC_API_KEY` | Claude Platform API key, used in preference to OpenRouter's | None |
| `OPENROUTER_API_KEY` | OpenRouter API key | None |

### Environment Variables (Server)

These are only relevant when running the server (`osa serve`):

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Server-side Claude Platform key | Required |
| `ANTHROPIC_BASE_URL` | AWS Marketplace endpoint; must be set with `ANTHROPIC_WORKSPACE_ID` | First-party default |
| `ANTHROPIC_WORKSPACE_ID` | Workspace the key is authorized on (`wrkspc_...`) | None |
| `DEFAULT_MODEL` | `claude-haiku-4-5` or `claude-sonnet-5` | `claude-haiku-4-5` |
| `OPENROUTER_API_KEY` | Server-side OpenRouter key, for a deployment funded that way instead | Optional |
| `LANGFUSE_PUBLIC_KEY` | LangFuse public key | Optional |
| `LANGFUSE_SECRET_KEY` | LangFuse secret key | Optional |
| `SYNC_ENABLED` | Enable automated knowledge sync | `true` |
| `GITHUB_TOKEN` | GitHub token for sync (higher rate limits) | Optional |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API key | Optional |
| `PUBMED_API_KEY` | PubMed/NCBI API key | Optional |
| `OPENALEX_EMAIL` | Email for OpenALEX polite pool | Optional |
| `DATA_DIR` | Data directory for knowledge DB | Platform-specific |

!!! note "Sync Schedules"
    Sync schedules are configured per-community in each community's `config.yaml` under the `sync` key, not via environment variables. See [Knowledge Sync](knowledge-sync.md) for details.

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

=== "macOS"

    ```bash
    export ANTHROPIC_API_KEY=sk-ant-your-key
    osa ask -a hed "What is HED?"
    osa chat -a bids
    ```

=== "Linux"

    ```bash
    export ANTHROPIC_API_KEY=sk-ant-your-key
    osa ask -a hed "What is HED?"
    osa chat -a bids
    ```

=== "Windows"

    ```powershell
    $env:ANTHROPIC_API_KEY = "sk-ant-your-key"
    osa ask -a hed "What is HED?"
    osa chat -a bids
    ```
