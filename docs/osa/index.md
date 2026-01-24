# Open Science Assistant (OSA)

An extensible AI assistant platform for researchers working with open science tools. Built with LangGraph/LangChain and FastAPI.

## Overview

OSA provides domain-specific AI assistants for open science tools (HED, BIDS, EEGLAB) with:

- **Modular tool system** for document retrieval, validation, and code execution
- **Multi-source knowledge bases** from GitHub, OpenALEX, Discourse forums, mailing lists
- **Extensible architecture** for adding new assistants and tools
- **Production-ready observability** via LangFuse

## Design Philosophy

- **Precision over features**: Researchers need accurate, citation-backed answers
- **Simple infrastructure**: Lab server deployment, no complex scaling
- **Extensible tools**: General tool system that communities can adapt
- **Domain expertise**: Deep knowledge of specific tools, not broad generalist

## Target Users

- Researchers learning HED annotations, BIDS formatting, or EEGLAB analysis
- Lab members needing quick, accurate answers from documentation
- Developers integrating these tools who need API/usage guidance

## Quick Start

```bash
# Clone the repository
git clone https://github.com/OpenScience-Collective/osa
cd osa

# Install dependencies
uv sync

# Run development server
uv run uvicorn src.api.main:app --reload --port 38528

# CLI usage
uv run osa --help

# Interactive chat with HED assistant
uv run osa chat -a hed

# Single query to HED assistant
uv run osa ask -a hed "How do I annotate a button press?"
```

## Specialist Assistants

| Assistant | Domain | Knowledge Sources |
|-----------|--------|-------------------|
| **HED Assistant** | Hierarchical Event Descriptors | hed-standard repos, hedtags.org |
| **BIDS Assistant** | Brain Imaging Data Structure | bids-standard repos, Neurostars |
| **EEGLAB Assistant** | EEG analysis toolbox | SCCN wiki, mailing lists |

## Documentation

- [Getting Started](getting-started.md) - Installation and setup
- [Architecture](architecture.md) - System design and diagrams
- [Community Registry](registry/index.md) - YAML-driven assistant configuration
    - [Adding a Community](registry/quick-start.md) - Add a new assistant in 5 minutes
    - [Schema Reference](registry/schema-reference.md) - Full YAML config reference
    - [Extensions](registry/extensions.md) - Python plugins and MCP servers
- [CLI Reference](cli-reference.md) - Command-line interface
- [API Reference](api-reference.md) - REST API documentation
- [Knowledge Sync](knowledge-sync.md) - Syncing GitHub, papers, and forums
- [Widget Deployment](deployment/widget.md) - Embed the chat widget
- [Tools](tools/index.md) - Available tools
- [Development](development.md) - Contributing to OSA

## External API Integrations

OSA integrates with existing validator and tool APIs rather than hosting validation engines locally:

| Service | API Endpoint | Integration |
|---------|--------------|-------------|
| HED Validation | https://hedtools.org/hed | String, sidecar, spreadsheet validation |
| BIDS Validator | https://bids-validator.github.io | Dataset structure validation |
| OpenALEX | https://api.openalex.org | Academic paper search |
| GitHub API | https://api.github.com | Issues, PRs, discussions |

## License

MIT
