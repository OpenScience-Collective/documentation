# OSA Platform Overview

An overview of the Open Science Assistant platform: architecture, community onboarding, knowledge pipeline, and roadmap.

## Recording

<div class="embed-container">
  <iframe
    src="https://www.youtube.com/embed/Uo0xQZMx534"
    title="OSA Platform Overview - Recording"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>

## Interactive Slides

<div class="embed-container">
  <iframe
    src="../slides/osa-platform/presentation.html?presentation=./osa-platform.json"
    title="OSA Platform Overview - Slides"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>

<p class="slide-hint">Use arrow keys to navigate. Press <kbd>F</kbd> for fullscreen, <kbd>?</kbd> for shortcuts.</p>

<style>
.embed-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
  overflow: hidden;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
.embed-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}
.slide-hint {
  margin: -0.5rem 0 1.5rem 0;
  font-size: 0.75rem;
  color: var(--md-default-fg-color--lighter);
}
.slide-hint kbd {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 3px;
  background: var(--md-code-bg-color);
}
</style>

## Summary

The Open Science Assistant is an extensible AI platform that serves small research communities from a single lab server. Key points covered:

- **Design philosophy**: Precision over features; researchers need accurate, citation-backed answers
- **Architecture**: Cloudflare Worker edge proxy, FastAPI + LangGraph backend, SQLite FTS5 knowledge stores
- **Community onboarding**: One YAML file creates a full AI assistant with API routes, tools, and knowledge sync
- **6 live communities**: HED, EEGLAB, BIDS, MNE-Python, NEMAR, FieldTrip
- **Two-tier tool system**: Auto-generated knowledge tools from YAML plus custom Python plugins
- **Knowledge pipeline**: 5 sources (GitHub, OpenALEX, mailing lists, Discourse, docstrings) synced into per-community databases
- **Smart FAQ generation**: Two-stage LLM pipeline reducing costs by ~85%
- **Embeddable widget**: One script tag to add an AI assistant to any project website
- **Future directions**: Multi-assistant delegation across communities, ephemeral preview backends for self-service onboarding

---

<small>Interactive slides built with [Agentic Presentation Builder](https://github.com/casual-vibers/agent-presentation), a JSON-to-Reveal.js presentation tool.</small>
