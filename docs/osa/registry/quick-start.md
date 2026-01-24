# Adding a New Community

This tutorial walks through adding a new research community assistant to OSA. By the end, you'll have a working assistant with documentation retrieval and API endpoints.

## Prerequisites

- OSA repository cloned and dependencies installed (`uv sync`)
- Familiarity with your community's documentation sources

## Step 1: Create the Community Directory

Create a directory under `src/assistants/` using your community's ID (kebab-case, lowercase):

```bash
mkdir -p src/assistants/my-tool/
```

## Step 2: Write config.yaml

Create `src/assistants/my-tool/config.yaml` with your community's configuration:

```yaml
# src/assistants/my-tool/config.yaml

id: my-tool
name: My Tool
description: A research tool for computational neuroscience
status: available

system_prompt: |
  You are a technical assistant specialized in My Tool.
  You provide explanations, troubleshooting, and guidance.

  {preloaded_docs_section}

  {available_docs_section}

  {page_context_section}

  {additional_instructions}

documentation:
  # Core docs (preloaded into system prompt)
  - title: Getting Started
    url: https://my-tool.org/docs/getting-started
    source_url: https://raw.githubusercontent.com/org/my-tool/main/docs/getting-started.md
    preload: true
    category: core
    description: Introduction and setup guide

  # On-demand docs (fetched via retrieve_docs tool)
  - title: API Reference
    url: https://my-tool.org/docs/api
    source_url: https://raw.githubusercontent.com/org/my-tool/main/docs/api.md
    category: reference
    description: Complete API documentation

  - title: Configuration Guide
    url: https://my-tool.org/docs/config
    source_url: https://raw.githubusercontent.com/org/my-tool/main/docs/config.md
    category: guides
    description: Configuration options and examples

# GitHub repos to sync issues/PRs from
github:
  repos:
    - org/my-tool
    - org/my-tool-plugins

# Paper search and citation tracking
citations:
  queries:
    - "my tool neuroscience"
    - "my tool analysis"
  dois:
    - "10.1234/example.2024.001"
```

## Step 3: Verify the Configuration

Run the tests to validate your config loads correctly:

```bash
uv run pytest tests/test_core/ -k "community" -v
```

You can also verify programmatically:

```python
from pathlib import Path
from src.core.config.community import CommunityConfig

config = CommunityConfig.from_yaml(
    Path("src/assistants/my-tool/config.yaml")
)
print(f"Loaded: {config.name} with {len(config.documentation)} docs")
```

## Step 4: Test the Assistant

Start the development server and test:

```bash
# Start the server
uv run uvicorn src.api.main:app --reload --port 38528

# Test the endpoint
curl -X POST http://localhost:38528/my-tool/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is My Tool?"}'
```

The registry auto-discovers your config and creates the `/{community-id}/ask` and `/{community-id}/chat` endpoints.

## Step 5: Sync Knowledge (Optional)

If you configured GitHub repos or citations, sync the knowledge database:

```bash
# Sync GitHub issues/PRs
uv run osa sync github --community my-tool

# Sync papers and citations
uv run osa sync papers --community my-tool --citations

# Or sync everything
uv run osa sync all --community my-tool
```

## Step 6: Deploy the Widget (Optional)

Add the chat widget to your community's website:

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'my-tool',
    title: 'My Tool Assistant',
    initialMessage: 'Hi! I can help with My Tool. What would you like to know?',
    placeholder: 'Ask about My Tool...',
    suggestedQuestions: [
      'How do I get started?',
      'What are the configuration options?',
      'How do I use the API?'
    ]
  });
</script>
```

See the [Widget Deployment Guide](../deployment/widget.md) for more options.

## What You Get

After completing these steps, your community has:

- **API endpoints**: `POST /my-tool/ask` and `POST /my-tool/chat`
- **Auto-generated tools**: `retrieve_my_tool_docs` with all your configured docs
- **Knowledge search**: GitHub issues/PRs and academic papers (after sync)
- **CLI access**: `osa ask -a my-tool "question"` and `osa chat -a my-tool`
- **Widget support**: Embeddable chat widget for your website

## Next Steps

- Add [specialized tools](extensions.md) for your community (e.g., validation APIs)
- Configure the [system prompt](schema-reference.md#system_prompt) with domain-specific instructions
- Set up [automated sync](../knowledge-sync.md) via the scheduler
