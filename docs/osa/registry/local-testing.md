# Local Testing Guide

This guide covers testing a new or modified community configuration locally before deploying.

## Prerequisites

- OSA repository cloned and dependencies installed (`uv sync`)
- A Claude Platform API key, either the platform's or your community's own (see [Getting Started](../getting-started.md#configuration)); an OpenRouter key works too if that is how your community funds itself
- Your community `config.yaml` created (see [Adding a Community](quick-start.md))

## 1. Validate Configuration

Before starting the server, check the config the way CI does:

```bash
# Schema, env vars, and referenced URLs
uv run osa validate --community my-tool

# Or point at the file directly, and test the key it names
uv run osa validate src/assistants/my-tool/config.yaml --test-api-key
```

`--test-api-key` calls the provider's models endpoint with whichever key the
config names, Anthropic or OpenRouter, so a key that is present but not
authorized is caught here rather than on the first question.
The probe is a plain listing, so it costs nothing.

You can also validate programmatically:

```python
from pathlib import Path
from src.core.config.community import CommunityConfig

config = CommunityConfig.from_yaml(
    Path("src/assistants/my-tool/config.yaml")
)
print(f"Loaded: {config.name} with {len(config.documentation)} docs")
```

Common validation errors and fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| `Community ID must be kebab-case` | Uppercase or underscore in ID | Use lowercase with hyphens |
| `DocSource has preload=True but no source_url` | Missing fetch URL | Add `source_url` field |
| `Repository must be in 'org/repo' format` | Invalid repo format | Use `organization/repository` |
| `Invalid DOI format` | Malformed DOI | Use `10.xxxx/yyyy` format |

## 2. Set Environment Variables

=== "macOS"

    ```bash
    # Required: Claude Platform key for LLM calls
    export ANTHROPIC_API_KEY="sk-ant-your-key"

    # Required with an AWS Marketplace key, and only as a pair
    export ANTHROPIC_BASE_URL="https://aws-external-anthropic.us-east-2.api.aws"
    export ANTHROPIC_WORKSPACE_ID="wrkspc_your-workspace-id"

    # Optional: API keys for admin functions (sync triggers)
    export API_KEYS="test-key-123"

    # Optional: your community's own funded key, named after the community
    # export ANTHROPIC_API_KEY_MY_TOOL="sk-ant-community-key"
    ```

=== "Linux"

    ```bash
    # Required: Claude Platform key for LLM calls
    export ANTHROPIC_API_KEY="sk-ant-your-key"

    # Required with an AWS Marketplace key, and only as a pair
    export ANTHROPIC_BASE_URL="https://aws-external-anthropic.us-east-2.api.aws"
    export ANTHROPIC_WORKSPACE_ID="wrkspc_your-workspace-id"

    # Optional: API keys for admin functions (sync triggers)
    export API_KEYS="test-key-123"

    # Optional: your community's own funded key, named after the community
    # export ANTHROPIC_API_KEY_MY_TOOL="sk-ant-community-key"
    ```

=== "Windows"

    ```powershell
    # Required: Claude Platform key for LLM calls
    $env:ANTHROPIC_API_KEY = "sk-ant-your-key"

    # Required with an AWS Marketplace key, and only as a pair
    $env:ANTHROPIC_BASE_URL = "https://aws-external-anthropic.us-east-2.api.aws"
    $env:ANTHROPIC_WORKSPACE_ID = "wrkspc_your-workspace-id"

    # Optional: API keys for admin functions (sync triggers)
    $env:API_KEYS = "test-key-123"

    # Optional: your community's own funded key, named after the community
    # $env:ANTHROPIC_API_KEY_MY_TOOL = "sk-ant-community-key"
    ```

## 3. Start the Development Server

```bash
uv run uvicorn src.api.main:app --reload --port 38528
```

The `--reload` flag enables auto-restart on file changes, so you can edit `config.yaml` and see results immediately.

## 4. Test Endpoints

### List all communities

Verify your community appears in the registry:

```bash
curl http://localhost:38528/communities | jq
```

Expected: your community appears with status `available`.

### Get community info

```bash
curl http://localhost:38528/communities/my-tool | jq
```

Expected response includes documentation count, repo count, and sync config status.

### Ask a question

```bash
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is My Tool?"
  }' | jq
```

### Test chat endpoint

```bash
curl -X POST http://localhost:38528/my-tool/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I get started?",
    "stream": false
  }' | jq
```

Pass the `session_id` from the response on the next turn to continue the same
conversation.

### Test with your own key

Neither request above names a key: the server uses the community's key, or the
platform's. To test the bring-your-own-key path instead, send the key as a
header. It is never a body field.

```bash
# Claude Platform key
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -H "X-Anthropic-API-Key: sk-ant-your-key" \
  -d '{"question": "What is My Tool?", "model": "claude-sonnet-5"}' | jq

# OpenRouter key, which is also what lets you name a non-Claude model
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: sk-or-v1-your-key" \
  -d '{"question": "What is My Tool?"}' | jq
```

## 5. Test via CLI

The CLI is often easier for interactive testing.
It talks to a server rather than running the assistant itself, so keep the
development server from step 3 running and point the CLI at it with
`--api-url`; its default is the hosted API.

=== "macOS"

    ```bash
    # Interactive chat against your local server
    uv run osa chat -a my-tool --api-url http://localhost:38528

    # Single question
    uv run osa ask -a my-tool "What is My Tool?" --api-url http://localhost:38528
    ```

=== "Linux"

    ```bash
    # Interactive chat against your local server
    uv run osa chat -a my-tool --api-url http://localhost:38528

    # Single question
    uv run osa ask -a my-tool "What is My Tool?" --api-url http://localhost:38528
    ```

=== "Windows"

    ```powershell
    # Interactive chat against your local server
    uv run osa chat -a my-tool --api-url http://localhost:38528

    # Single question
    uv run osa ask -a my-tool "What is My Tool?" --api-url http://localhost:38528
    ```

To save the URL instead of passing it every time:
`uv run osa config set --api-url http://localhost:38528`.

The CLI always sends a key of its own, from `-k`, the environment, or
`osa init`, and refuses to run without one.
That key is a BYOK header on the wire, so a CLI question bills you rather than
the community: to exercise the community's own key, use the curl requests above
or the widget.

## 6. Verify Documentation Retrieval

Test that the assistant retrieves documentation correctly by asking specific questions that require doc lookup:

```bash
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I configure advanced settings?",
    "stream": false
  }' | jq
```

Check that:

- The response references your documentation sources
- Links in the response point to valid URLs
- Preloaded docs are used without tool calls
- On-demand docs trigger the `retrieve_*_docs` tool
- Claims drawn from a retrieved document carry an inline `[n]`, and the matching
  entry in the `citations` array names that document, with a `cited_text` span
  you can find in it

Preloaded documents are the one exception: they travel in the system prompt,
which cannot be cited, so an answer built entirely from a preloaded overview
carries no marker. That is a reason to keep the preload list short.

## 7. Sync Knowledge Database (Optional)

If you configured GitHub repos or citations, test the sync:

```bash
# Initialize the knowledge database for your community
uv run osa sync init --community my-tool

# Sync GitHub issues and PRs
uv run osa sync github --community my-tool --full

# Sync papers (includes citation tracking by default)
uv run osa sync papers --community my-tool

# Or sync everything at once
uv run osa sync all --community my-tool
```

After syncing, test knowledge search:

```bash
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the latest issues?"
  }' | jq
```

## What Works Without Sync

| Feature | Without sync | With sync |
|---------|-------------|-----------|
| Assistant creation | Yes | Yes |
| System prompt | Yes | Yes |
| Documentation retrieval | Yes | Yes |
| Answering questions | Yes | Yes |
| GitHub issues/PRs search | No | Yes |
| Recent activity listing | No | Yes |
| Paper search | No | Yes |
| Citation counts | No | Yes |

## Troubleshooting

### Server won't start

=== "macOS"

    ```bash
    # Check if port is already in use
    lsof -i :38528

    # Use a different port
    uv run uvicorn src.api.main:app --reload --port 38529
    ```

=== "Linux"

    ```bash
    # Check if port is already in use
    lsof -i :38528

    # Use a different port
    uv run uvicorn src.api.main:app --reload --port 38529
    ```

=== "Windows"

    ```powershell
    # Check if port is already in use
    netstat -ano | findstr :38528

    # Use a different port
    uv run uvicorn src.api.main:app --reload --port 38529
    ```

### "Assistant not found" error

Verify your community is discovered:

```bash
uv run python -c "
from src.assistants import discover_assistants, registry
discover_assistants()
print('my-tool' in registry)
print([a.id for a in registry.list_available()])
"
```

Common causes:

- Directory not under `src/assistants/`
- Missing or invalid `config.yaml`
- YAML syntax errors (check with `python -c "import yaml; yaml.safe_load(open('path/to/config.yaml'))"`)

### Documentation not retrieved

- Check network access to documentation URLs
- Verify `source_url` fields are valid raw GitHub URLs
- Test URLs manually: `curl -I <source_url>` should return 200

### Knowledge base empty

- Requires `API_KEYS` env var for sync operations
- Run `uv run osa sync init --community my-tool` first
- Check that GitHub repos in config are accessible (public repos)

### Preloaded docs too large

If the server is slow to start or the system prompt is very long:

- Limit preloaded docs to 2-3 core documents
- Keep total preloaded content under 15k tokens
- Move large docs to on-demand retrieval

## Test Checklist

Use this checklist when testing a new community:

- [ ] Config validates without errors (`osa validate --community my-tool`)
- [ ] Community appears in `/communities` endpoint
- [ ] Community info endpoint returns correct metadata
- [ ] `/ask` endpoint returns relevant answers
- [ ] `/chat` endpoint works for multi-turn conversations
- [ ] Preloaded documentation is used correctly
- [ ] On-demand docs are retrieved when relevant
- [ ] Documentation URLs in responses are valid
- [ ] Answers carry inline `[n]` citations, and each one points at the document the claim came from (`citations` in the response body)
- [ ] CLI reaches the local server (`osa ask -a my-tool ... --api-url http://localhost:38528`)
- [ ] Knowledge sync completes (if configured)
- [ ] GitHub issues/PRs are searchable (after sync)
- [ ] Paper search works (after sync)
- [ ] Anti-hallucination: assistant does not fabricate PR/issue numbers
