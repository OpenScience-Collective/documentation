# UC Open 2026 — A community-owned AI model for research tools

A 15-minute talk at the [UC Open 2026 summit](https://ucospo.net/events/uc-open-2026) in Berkeley, April 22–23, 2026. Condensed from the long-form OSA platform overview.

## Interactive Slides

<div class="embed-container">
  <iframe
    src="../slides/uc-open-2026/presentation.html?presentation=./uc-open-2026.json"
    title="UC Open 2026 - Open Science Assistant"
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

## Abstract

Research tools like BIDS, EEGLAB, MNE-Python, and HED depend on a handful of maintainers, scattered documentation, and forums that are easy to miss. General-purpose AI assistants hallucinate tool-specific answers. Each community is too small to build a bespoke AI on its own.

The Open Science Collective (OSC) treats this as a shared-infrastructure problem. The Open Science Assistant (OSA) is the AI layer of that infrastructure: one platform, one FastAPI + LangGraph agent loop, one SQLite FTS5 store per community, and a YAML file that onboards the next community in an afternoon. Seven assistants are live today; EEGLAB alone has answered over sixteen hundred questions at a 99% success rate, peaking above 100 questions a day.

The talk covers:

- **Why the OSC model works** for small research communities that cannot each fund their own AI stack
- **The friction** on both sides: stagnant communities with rotting docs, and general AI that hallucinates
- **Architecture** that avoids the usual Retrieval-Augmented Generation (RAG) failure modes: source of truth is the live community (GitHub, docs, papers, mailing lists), re-synced on every PR, issue, or doc update, with citations by construction and Anthropic prompt caching for ~90% cost savings on system and repeated prompts
- **YAML-driven onboarding**: a single file creates the assistant, API routes, embeddable widget, and knowledge sync job
- **Public status** at [status.osc.earth/osa](https://status.osc.earth/osa): aggregate + per-community metrics, sync health, and usage charts
- **How to join**: file an issue, open the Discord, or drop a YAML

## Links

- **Platform code**: [github.com/OpenScience-Collective/osa](https://github.com/OpenScience-Collective/osa)
- **Documentation**: [docs.osc.earth/osa](https://docs.osc.earth/osa)
- **Live demo**: [demo.osc.earth](https://demo.osc.earth)
- **Status dashboard**: [status.osc.earth/osa](https://status.osc.earth/osa)
- **Event**: [UC Open 2026](https://ucospo.net/events/uc-open-2026)

---

<small>Interactive slides built with [Agentic Presentation Builder](https://github.com/casual-vibers/agent-presentation), a JSON-to-Reveal.js presentation tool.</small>
