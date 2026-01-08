# Open Science Collective

Welcome to the documentation for the **Open Science Collective** (OSC) and its projects.

## What is OSC?

The Open Science Collective is a community-driven initiative dedicated to building open-source tools and infrastructure for scientific research. We focus on precise, reliable tools for small research communities, built for accuracy over scale.

## Our Projects

<div class="grid cards" markdown>

-   :material-robot:{ .lg .middle } **Open Science Assistant (OSA)**

    ---

    An extensible AI assistant platform for researchers working with open science tools. Provides domain-specific AI assistants for HED, BIDS, and EEGLAB with modular tools, open API, and extensible CLI.

    [:octicons-arrow-right-24: OSA Documentation](osa/index.md)

-   :material-account-group:{ .lg .middle } **The Collective**

    ---

    Learn about the Open Science Collective, our mission, and how to contribute to our projects.

    [:octicons-arrow-right-24: About Us](collective/index.md)

</div>

## Quick Links

- [About Us](collective/about.md) - Learn about our organization
- [OSA Getting Started](osa/getting-started.md) - Set up the Open Science Assistant
- [OSA Architecture](osa/architecture.md) - System design and diagrams
- [Contributing](collective/contributing.md) - Join our community

## Featured: Open Science Assistant

OSA provides domain-specific AI assistants for open science tools with:

- **Precision over features**: Accurate, citation-backed answers researchers can trust
- **Simple infrastructure**: Lab server deployment without complex scaling
- **Extensible tools**: Modular tool system communities can adapt for their needs
- **Multi-source knowledge**: GitHub issues, OpenALEX papers, Discourse forums, documentation

```bash
# Quick start with OSA
uv sync
uv run osa --help

# Start the API server
uv run uvicorn src.api.main:app --reload --port 38528

# Interactive chat
uv run osa chat
```

## Target Research Communities

OSA serves multiple small research communities, each with specific tool needs:

| Community | Focus Area | Knowledge Sources |
|-----------|------------|-------------------|
| **HED** | Hierarchical Event Descriptors | hed-standard repos, hedtags.org |
| **BIDS** | Brain Imaging Data Structure | bids-standard repos, Neurostars |
| **EEGLAB** | EEG analysis toolbox | SCCN wiki, mailing lists |
