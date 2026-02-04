# Local Testing Guide

This guide covers testing a new or modified community configuration locally before deploying.

## Prerequisites

- OSA repository cloned and dependencies installed (`uv sync`)
- A valid OpenRouter API key (or community-specific key)
- Your community `config.yaml` created (see [Adding a Community](quick-start.md))

## 1. Validate Configuration

Before starting the server, verify your config loads correctly:

```bash
# Run community config tests
uv run pytest tests/test_core/ -k "community" -v
```

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

```bash
# Required: OpenRouter API key for LLM calls
export OPENROUTER_API_KEY="your-key-here"

# Optional: API keys for admin functions (sync triggers)
export API_KEYS="test-key-123"

# Optional: Community-specific key (if using BYOK)
# export OPENROUTER_API_KEY_MY_TOOL="community-specific-key"
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
    "question": "What is My Tool?",
    "api_key": "your-openrouter-key"
  }' | jq
```

### Test chat endpoint

```bash
curl -X POST http://localhost:38528/my-tool/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "How do I get started?"}
    ],
    "api_key": "your-openrouter-key"
  }' | jq
```

## 5. Test via CLI

The CLI is often easier for interactive testing:

```bash
# Set API key
export OPENROUTER_API_KEY="your-key-here"

# Interactive chat (standalone mode, no server needed)
uv run osa chat --community my-tool --standalone

# Single question
uv run osa ask --community my-tool "What is My Tool?" --standalone
```

The `--standalone` flag runs the assistant without needing the backend server.

## 6. Verify Documentation Retrieval

Test that the assistant retrieves documentation correctly by asking specific questions that require doc lookup:

```bash
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I configure advanced settings?",
    "api_key": "your-openrouter-key",
    "stream": false
  }' | jq
```

Check that:

- The response references your documentation sources
- Links in the response point to valid URLs
- Preloaded docs are used without tool calls
- On-demand docs trigger the `retrieve_*_docs` tool

## 7. Sync Knowledge Database (Optional)

If you configured GitHub repos or citations, test the sync:

```bash
# Initialize the knowledge database for your community
uv run osa sync init --community my-tool

# Sync GitHub issues and PRs
uv run osa sync github --community my-tool --full

# Sync papers and citations
uv run osa sync papers --community my-tool --citations

# Or sync everything at once
uv run osa sync all --community my-tool
```

After syncing, test knowledge search:

```bash
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the latest issues?",
    "api_key": "your-openrouter-key"
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

```bash
# Check if port is already in use
lsof -i :38528

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

- [ ] Config validates without errors (`pytest -k community`)
- [ ] Community appears in `/communities` endpoint
- [ ] Community info endpoint returns correct metadata
- [ ] `/ask` endpoint returns relevant answers
- [ ] `/chat` endpoint works for multi-turn conversations
- [ ] Preloaded documentation is used correctly
- [ ] On-demand docs are retrieved when relevant
- [ ] Documentation URLs in responses are valid
- [ ] CLI standalone mode works
- [ ] Knowledge sync completes (if configured)
- [ ] GitHub issues/PRs are searchable (after sync)
- [ ] Paper search works (after sync)
- [ ] Anti-hallucination: assistant does not fabricate PR/issue numbers
