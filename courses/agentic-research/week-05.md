# Week 5: Literature Search and Review

## Overview

A literature review is not a single prompt; it is a managed pipeline. Five stages, enforced order, bidirectional boomerang on review findings, citation grounding at every step. Same epic, sub-issue, and pull request rigor introduced in Week 3, plus a "cite-the-card" rule that makes hallucinated references mechanically impossible. The walkthrough at the end builds a working mini lit review on the neural correlates of naturalistic movie watching, organised by four perspectives: psychophysics, action, language, emotion.

The single most useful idea in this session: **a literature review has a Definition of Done.** Same way a feature branch is not "done" until continuous integration (CI) is green, a literature review is not "done" until every claim points at a stored paper-card and the review boomerang has run at least once. Convergence in one shot is a red flag, not a green flag.

!!! abstract "Learning Objectives"
    - Frame a literature review as a **5-stage pipeline**: direction, collect, synthesize, draft, review
    - Use `/project:epic-dev` to scope a review into parallel **strand briefs** (sub-issues) before any paper is read
    - Search and retrieve papers with `/opencite:opencite` and the `opencite` command-line interface (CLI): canonical works, recent work, citation graphs, batched portable document format (PDF) download, PDF-to-markdown conversion
    - Build a **paper-card corpus** with a uniform schema (one folder per paper, license-aware archival, BibTeX index, INDEX.md)
    - Produce **synthesis artefacts** before any prose: taxonomies, hierarchies, gap analysis
    - Draft a grounded review where every claim cites a paper-card by relative path
    - Run `/manuscript:paper-review` and treat reviewer findings as a **boomerang** that re-enters the pipeline at the direction or collection stage
    - Recognise the failure modes that make AI-assisted reviews look credible but are not, and the mechanical disciplines that prevent each

<div class="embed-container">
  <iframe
    src="https://www.youtube.com/embed/3SiigHNZMMs"
    title="Week 5: Literature Search and Review"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>


## Slides

<div class="embed-container">
  <iframe
    src="../../slides/agentic-research/week-05/presentation.html?presentation=./week-05.json"
    title="Week 5 Slides"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>

<p class="slide-hint">Use arrow keys to navigate. Press <kbd>F</kbd> for fullscreen, <kbd>?</kbd> for shortcuts.</p>


---

## Guide

The rest of this page walks through the workflow in the order the live session follows.

### 1. Why Structured Literature Reviews

Three failure modes that unstructured reviews fall into. Already common in manual reviews; agentic workflows accelerate each by an order of magnitude.

**String-of-pearls citation.** One paper, then the next paper, then the next paper. The text reads as well-cited from a distance and has no thematic spine when you actually read it. Each paragraph could be deleted without changing the argument. The review documents the literature instead of synthesising it.

**Recency bias.** The top of the search-result page becomes the field. Foundational work from 2010 is below the fold and never makes it into the draft. Agents make this worse because they accept the result-list ordering as canonical unless told to sort by citations or to call a `canonical` query first.

**Hallucinated references.** Plausible author, plausible year, plausible journal, plausible-sounding title, no such paper. Manual reviewers catch these in their own writing because they cited the paper themselves; agents cannot, because they did not.

!!! warning "AI raises the stakes"
    The fix is not "ask the agent to cite better." The fix is **structural**: a pipeline where every claim is mechanically traceable to a stored, retrievable artefact.

### 2. The 5-Stage Pipeline

```text
[ 1. Direction ] -> [ 2. Collect ] -> [ 3. Synthesize ] -> [ 4. Draft ] -> [ 5. Review ]
        ^                                                                       |
        +-----------------------------------------------------------------------+
                              boomerang on gaps
```

Five stages, enforced order. Drafting before synthesising is a structural error, not a style choice. Each stage has its own tools.

| Stage | Tool | Output |
|-------|------|--------|
| 1. Direction | `/project:epic-dev`, plan mode | Epic issue + per-strand briefs (sub-issues) |
| 2. Collect | `/opencite:opencite`, `opencite` CLI | `collection/<strand>/<slug>/` folders, `INDEX.md`, `.bib` |
| 3. Synthesize | `/opencite:literature-review`, manual cross-reference | Taxonomies, hierarchies, gap analysis |
| 4. Draft | `/manuscript:manuscript-formatting`, `/manuscript:manuscript-writing` | Mini-review with cite-the-card discipline |
| 5. Review | `/manuscript:paper-review` | Severity-tagged findings; boomerang back to Stage 1 or 2 |

!!! important "The boomerang is the rigor signal"
    A review that never updates the corpus has either nothing to say or is hiding what it found. A first-draft review that passes everything is a red flag, not a green flag.

### 3. Stage 1: Direction

The pattern is the same as Week 3: an epic issue with parallel sub-issues. The sub-issues here are called **strands**. Each strand is a concurrent collection pass with its own brief, branch, and pull request (PR).

!!! tip "Real-world example: Annotation Garden Initiative (AGI)"
    The canonical full-scale worked example is the AGI research foundation epic at [`Annotation-Garden/management#3`](https://github.com/Annotation-Garden/management/issues/3). Three strands (tools, data, science), three sub-issues, ~99 paper-cards across the corpus, five Phase 2 synthesis docs, three direction papers. The Week 5 practicum is a smaller-scoped reproduction sized to fit in one teaching session.

A **strand brief** has five fields. Treat each as a contract:

```markdown
## Goal
One sentence. The strand's main claim or coverage area.

## Scope
3-5 sub-areas the strand covers.

## Per-entry deliverable
What every paper-card folder must contain.

## Acceptance criteria
How we know the strand is done.

## Out-of-scope
What *not* to chase.
```

!!! info "Out-of-scope is the most under-used field"
    It tells the agent which adjacent rabbit-hole *not* to follow. Without it, Stage 2 collects whatever the first search surfaces.

For the practicum we use four strands organised by analytical perspective: psychophysics (low-level neural tracking of image and motion statistics), action (action observation under naturalistic viewing), language (speech and narrative comprehension), emotion (affective dynamics across viewers). The full strand briefs ship in [`sessions/week-05/practicum/_briefs/`](https://github.com/OpenScience-Collective/agentic-research-course/tree/main/sessions/week-05/practicum/_briefs).

### 4. Stage 2: Collect with `opencite`

Three search strategies. Combine them deliberately.

```bash
# Foundational, high-citation works (antidote to recency bias)
uvx opencite canonical "naturalistic stimuli EEG" --max 10

# Recent or specific
uvx opencite search "movie-watching EEG developmental" \
  --max 20 --sort citations

# Citation graph traversal (both directions)
uvx opencite cite "10.1126/science.1089506" --direction both
```

Two interfaces, one CLI underneath. The **`/opencite:opencite` skill** drives the workflow with judgement: it picks which strategy to use, evaluates the search results, decides which papers to download, and handles license-aware archival. The **`opencite` CLI** at [`github.com/neuromechanist/opencite`](https://github.com/neuromechanist/opencite) is a primitive that the skill calls underneath. Install with `uv pip install opencite` (persistent) or `uvx opencite` (one-off).

Batched retrieval and conversion in one go:

```bash
uvx opencite search "naturalistic EEG" --max 20 -f json -o results.json
uvx opencite batch-fetch \
  --from-json results.json \
  --convert -o ./papers \
  --summary report.json
```

Output tree:

```text
papers/
+-- pdf/
|     +-- paper-A.pdf       # open-access, committed
|     L-- paper-B.pdf       # paywalled, excluded by policy
+-- markdown/
|     +-- paper-A.md
|     +-- paper-B.md        # always present, even for paywalled papers
|     L-- img/
|           L-- paper-A/    # extracted figures (markit-mistral only)
L-- report.json
```

!!! warning "License-aware archival is non-negotiable"
    Open-access PDFs (CC-BY, CC0, arXiv, bioRxiv, OSF) commit; paywalled PDFs do not. Markdown extraction always commits, since extracted text is generally fair use for research notes. The `redistribution_ok` flag in `meta.json` is the single source of truth.

### 5. The Paper-Card Schema

Each paper lives in its own folder:

```text
collection/<strand>/<slug>/
+-- card.md         the paper-card; required
+-- source.pdf      full PDF, only when redistributable
+-- source.md       markdown extraction, always required
L-- meta.json       provenance: source URL, retrieval date, license, hash
```

The `card.md` template:

```yaml
---
slug: hasson-2004-isc
type: paper
strand: psychophysics
year: 2004
authors: [Hasson, Nir, Levy, Fuhrmann, Malach]
venue: Science
doi: 10.1126/science.1089506
license: publisher-paywall
modalities: [fmri]
tags: [intersubject-correlation, naturalistic-viewing, foundational]
relevance: high
pdf_status: not-redistributable
md_path: source.md
md_quality: abstract-only
---

## TL;DR
One or two sentences. The thesis, not the abstract opening.

## Summary
3-6 sentences covering core contribution, method, scope, key numbers.

## Relevance
Concrete connection to the strand. Cite specific mechanisms.

## Notable details
Bullet list of facts worth pulling forward to synthesis.

## Open questions
What this work does not answer. Paper-specific only.

## Citations
Primary BibTeX key plus up to 5 related works as one-liners.
```

Six required sections. Generic "this is relevant because..." prose is not acceptable in the Relevance section; the agent must cite specific mechanisms (band, network, paradigm, dataset). Open Questions feeds Phase 2 gap analysis directly; skip it and synthesis becomes much harder.

!!! important "The schema is the rigor discriminator"
    With it, the corpus is queryable and uniform. Without it, every entry is a free-form note that downstream steps cannot rely on.

### 6. Calibration Anchors

The `relevance` field is useful only if it discriminates. Spell out anchor examples in the schema:

- **high.** Direct dependency of the strand's main claim. Example: an electroencephalography (EEG) study that defines the standard analysis for the strand.
- **medium.** Standard work in scope, not the anchor. Example: a functional magnetic resonance imaging (fMRI) study on the same perspective whose findings need EEG translation.
- **low.** Tangential or background context.

!!! tip "Recalibrate when one bucket gets crowded"
    If more than ~40% of entries land at one level, the field has lost discriminative power; recalibrate. Same logic applies to any rated field. Calibration anchors are the cheapest mechanical defence against thumb-on-scale: no prompt engineering, no review process, just anchor examples in the schema.

### 7. Stage 3: Synthesize -- Structure Before Prose

The most-skipped stage. The temptation is to draft as soon as you have papers. Resist.

Synthesis produces structured artefacts only: tables, hierarchies, maps, gap analysis, scope diagrams. AGI's Phase 2 produced five docs:

- **Tool ontology.** Hierarchical map of the 33 tool, platform, and standard entries grouped into five layers.
- **Dataset hierarchy.** Formal placement of all 36 dataset entries along a naturalistic / cognitive-task spectrum.
- **Science map.** Methodological themes across the 30 science papers.
- **Gap analysis.** Three-column comparison of coverage across two scopes and the uncovered terrain.
- **Scope diagram.** Side-by-side dimensions and the explicit complementarity statement.

For the practicum the synthesis layer is smaller: a perspective-by-method matrix and a one-row-per-strand gap analysis ([`synthesis/gap-analysis-stub.md`](https://github.com/OpenScience-Collective/agentic-research-course/blob/main/sessions/week-05/practicum/synthesis/gap-analysis-stub.md)).

!!! info "The gap analysis is the bridge to Stage 4"
    It names the claims the prose review will defend. If you cannot fill in a row, you do not have a claim.

### 8. Stage 4a: `/manuscript:manuscript-formatting`

Picks the structure. Five common review types, each with different rules:

| Type | Purpose | Method | Output |
|------|---------|--------|--------|
| **Mini-review** | Focused review for a specific question | Targeted search | Brief, focused synthesis |
| **Scoping** | Map the extent of literature on a topic | Broad search, categorisation | Overview of themes and gaps |
| **Narrative** | Summarise and interpret a body of literature | Selective, thematic | Flowing prose with arguments |
| **Systematic** | Exhaustive, reproducible search | PRISMA protocol | Structured report |
| **IMRAD background** | Introduction section of a manuscript or grant | Embedded | Argument paragraph |

The practicum uses the mini-review structure. Week 6 (grants) and Week 7 (manuscripts) revisit this skill for IMRAD; today the focus is the lit review as a standalone artefact.

### 9. Stage 4b: `/manuscript:manuscript-writing` -- The Cite-the-Card Rule

Two prose rules above all others.

**Thematic, not chronological.** Group paragraphs by argument, not by year. Chronological organisation only works when the timeline is itself the argument; otherwise it disguises a string-of-pearls.

**Cite the card.** Every claim cites a paper-card by relative path. If the agent cannot link to a `card.md`, the claim does not appear in the draft.

!!! important "Hallucinated citations are mechanically impossible"
    With the cite-the-card rule, every claim points to a stored card whose existence is verifiable. This is the second mechanical defence against thumb-on-scale.

Citation weaving comes in four shapes:

- **Integral.** "Hasson and colleagues showed that ~30% of cortex synchronises across viewers under naturalistic viewing [card]."
- **Non-integral.** "Approximately one-third of cortex is engaged in synchronised activity during free viewing [card]."
- **Synthesis.** "Multiple lines of evidence converge on the conclusion that editorial control predicts intersubject correlation [card-A] [card-B] [card-C]."
- **Contrast.** "Where Hasson 2008 reports near-perfect synchronisation [card-A], Bartels and Zeki 2004 report substantially noisier signals [card-B]."

Real examples in the AGI direction papers ([`direction-papers/science-direction.md`](https://github.com/Annotation-Garden/management/blob/main/direction-papers/science-direction.md)) -- about 30 cite-the-card links across ~160 lines.

### 10. Stage 5: Review and the Boomerang

`/manuscript:paper-review` plays the peer-reviewer role: methodological rigor, statistical validity, balance, scope creep. Findings are tagged by severity (critical, major, minor). Critical and major findings cycle back into the pipeline:

- **Missing evidence -> Stage 2.** The reviewer surfaced a claim the corpus does not support; go collect more papers.
- **Mis-scoped direction -> Stage 1.** The reviewer surfaced that the strand brief left a gap; revise the brief and re-run collection.

This is the **boomerang**: the rigor signal that distinguishes a managed pipeline from a one-shot prompt.

!!! warning "Convergence in one shot is a red flag"
    A first-draft review that passes everything either means the review is shallow or the corpus is hiding what it found. Run again with adversarial framing if the first pass converges too cleanly.

### 11. Three Defences Against Thumb-on-Scale

The three rigor defences are deliberately stack-redundant, one per stage:

- **Calibration anchors** at scoring time (Stage 2). Cheap and mechanical.
- **Cite-the-card** at drafting time (Stage 4). Makes hallucination structurally impossible.
- **Boomerang** at review time (Stage 5). Cycles the corpus, not just the prose.

Each catches a different failure mode at a different stage. None alone is sufficient. The combination produces a review that lands its conclusion through evidence, irrespective of whether the evidence supports the working hypothesis or contradicts it. **Bias-irrespective rigor.**

### 12. Live Walkthrough

The Week 5 session ends with a live walkthrough on the practicum scaffold at [`sessions/week-05/practicum/`](https://github.com/OpenScience-Collective/agentic-research-course/tree/main/sessions/week-05/practicum).

Topic: literature review on the neural correlates of naturalistic movie watching, organised by four perspectives (psychophysics, action, language, emotion). Extends the Week 3 Healthy Brain Network (HBN) movie-watching practicum.

Pre-built state:

- Epic brief
- Four strand briefs, one per perspective
- Four anchor cards: Hasson 2004 (psychophysics), Hasson 2008 (action), Huth 2016 (language), Saarimaki 2016 (emotion). Each card is schema-compliant with real digital object identifier (DOI), license, and provenance metadata.
- A synthesis stub with a one-row-per-strand gap analysis
- A direction-paper draft stub with a thesis paragraph slot and a section skeleton

Three live actions:

1. **Add one new paper.** Pick a 2024-2026 open-access paper from any of the four strands. Run the `/opencite:opencite` skill with the DOI; it should produce `card.md`, `source.md`, `meta.json` in `collection/<strand>/<slug>/`, append to the strand `INDEX.md`, and add a BibTeX entry to the strand `.bib`.

2. **Weave one paragraph.** Run `/manuscript:manuscript-writing` to integrate the new paper into one synthesis paragraph in `direction-paper/draft-stub.md`. Every claim cites a paper-card by relative path.

3. **Run the review.** Run `/manuscript:paper-review` on that paragraph. Whatever the review surfaces, walk through. We do not manufacture a gap. If a real one appears (a likely natural one given HBN's developmental cohort and the seed-card distribution is **age-effect / developmental coverage**), we describe the boomerang back to Stage 2 with a follow-on `opencite search` call -- but do not run it on stage; we stay in the time box.

!!! important "The boomerang is the teaching moment"
    A red review finding is more reassuring for a first-time literature-review-pipeline user than a clean draft, because it proves the system actually catches things.

### 13. Before Next Week

- Install `opencite` as a one-off (`uvx opencite --version`) or persistently (`uv pip install opencite`).
- Add the [`research-skills`](https://github.com/neuromechanist/research-skills) plugin if not already installed; it bundles `opencite`, `manuscript`, and `project`.
- Pick a topic in your own research area where a focused mini lit review (15-30 papers) would actually move your work forward.
- Optional: skim two of the AGI direction papers ([`science-direction.md`](https://github.com/Annotation-Garden/management/blob/main/direction-papers/science-direction.md) and [`tools-direction.md`](https://github.com/Annotation-Garden/management/blob/main/direction-papers/tools-direction.md)) to see what the end of the pipeline looks like at full scale.
- Make sure your repo has a long-lived branch (`develop` or equivalent) where the lit review epic can land separately from `main`.

Week 6 starts from the corpus produced here. A grant Specific Aims page is, structurally, a literature review condensed into one page; the cards and bibliography from this week feed directly into next week's drafting.

---

## Resources

**Course materials**

- [Week 5 session](https://github.com/OpenScience-Collective/agentic-research-course/tree/main/sessions/week-05)
- [Week 5 practicum](https://github.com/OpenScience-Collective/agentic-research-course/tree/main/sessions/week-05/practicum)
- [Week 5 blog (markdown source)](https://github.com/OpenScience-Collective/agentic-research-course/blob/main/blog/week-05-literature-review.md)
- [Course repository](https://github.com/OpenScience-Collective/agentic-research-course)
- [research-skills plugin](https://github.com/neuromechanist/research-skills) (bundles `opencite`, `manuscript`, `project`)

**External references**

- [opencite CLI](https://github.com/neuromechanist/opencite)
- [Annotation Garden Initiative research foundation epic](https://github.com/Annotation-Garden/management/issues/3) (full-scale worked example)
- [AGI direction papers](https://github.com/Annotation-Garden/management/tree/main/direction-papers)
- [Open Science Collective Discord](https://discord.gg/5dWJCUmUww)

<style>
.embed-container {
  position: relative;
  padding-bottom: 56.25%;
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
