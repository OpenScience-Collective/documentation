# Agentic Research Course

A 10-week live course teaching researchers how to use Claude Code and AI coding agents for academic research workflows, hosted by the [Open Science Collective](https://osc.earth).

## Format

- **Sessions:** 30-45 min live + 15 min Q&A
- **Schedule:** Wednesdays at 9:00 AM Pacific / 12:00 PM Eastern / 4:00 PM UTC
- **Dates:** April 8 -- June 9, 2026
- **Zoom:** [Join via Zoom](https://ucsd.zoom.us/j/93199206194)
- **Nextcloud Talk:** [Join via Nextcloud](https://skynas.tail75926.ts.net/call/z2qi8v6g) (alternative for those without Zoom access)
- **Office Hours:** Fridays 9-10 am PT, [Join via Zoom](https://ucsd.zoom.us/j/91024610601)
- **Recordings:** Uploaded to [YouTube](https://www.youtube.com/@neuromechanist) after each session
- **Community:** [Discord](https://discord.gg/5dWJCUmUww) (OpenScience Collective)
- **Plugin:** [research-skills](https://github.com/neuromechanist/research-skills) (free, open source)
- **Source:** [GitHub](https://github.com/OpenScience-Collective/agentic-research-course)
- **License:** CC-BY-4.0

<a target="_blank" href="https://calendar.google.com/calendar/event?action=TEMPLATE&amp;tmeid=M3RmMG83bG9lbXZ0YzRmc2VxOWY4dmphbG5fMjAyNjA0MTVUMTYwMDAwWiBzaGlyYXppQGllZWUub3Jn&amp;tmsrc=shirazi%40ieee.org&amp;scp=ALL"><img border="0" src="https://calendar.google.com/calendar/images/ext/gc_button1_en.gif" alt="Add to Google Calendar"></a>

## Schedule

| Date | Session | Topic |
|------|---------|-------|
| Wed April 8 | [Week 1](week-01.md) | Git, GitHub, and the Command Line |
| Wed April 15 | [Week 2](week-02.md) | Setting Up Claude Code for Research |
| **Tue** April 21 | [Week 3](week-03.md) | Project Management with AI |
| Wed April 29 | [Week 4](week-04.md) | CI/CD and Code Quality |
| Wed May 6 | [Week 5](week-05.md) | Literature Search and Review |
| Wed May 13 | [Week 6](week-06.md) | Grant Proposal Writing |
| Wed May 20 | [Week 7](week-07.md) | Manuscript Preparation and Peer Review |
| Wed May 27 | [Week 8](week-08.md) | Scientific Figures |
| Wed June 3 | Week 9 | Neuroinformatics |
| **Tue** June 9 | Week 10 | Building Your Own Plugins |

## Prerequisites

- A computer with terminal access (macOS, Linux, or Windows Subsystem for Linux (WSL))
- A [GitHub](https://github.com) account (free)
- No prior coding experience required for Weeks 1-2

## Practicum: A Real Research Project

Every workflow in this course is demonstrated against an actual open research question, not a toy dataset. The practicum asks: **is there a group-level electroencephalography (EEG) signature locked to movie shot changes, and does it depend on what is in the shot?**

Concretely, we compare event-related spectral perturbation (ERSP) in the first 500 ms after shot onset between shots in the Pixar short *"The Present"* that open with the boy visible against shots that open with the puppy visible. The contrast isolates content-driven brain responses (animacy, social attention) from low-level visual-onset effects that every shot change shares.

The dataset is the published [Healthy Brain Network (HBN) EEG Release 3](https://nemar.org/dataexplorer/detail?dataset_id=ds005507) on NEMAR and OpenNeuro: 183 children and adolescents watching *The Present*, 128-channel high-density EEG, formatted with Brain Imaging Data Structure (BIDS) and annotated with Hierarchical Event Descriptors (HED). Shot-level annotations come from the EventFormer project (Shirazi lab): 56 shots with frame-level descriptions, log-luminance-ratio, and content flags (`has_boy`, `has_puppy`).

This is not a reproduction of an existing result. The boy-versus-puppy ERSP contrast has not been published for this dataset, and the animacy-of-opening-shot question is genuinely open. The deliverable is a reproducible pipeline (BIDS import -> cleaning -> adaptive mixture independent component analysis (AMICA) -> IClabel -> shot-aligned epoching -> ERSP -> cluster-level statistics) plus a publication-quality figure of the group contrast. The instructor drives the analysis live each week using EEGLAB plus [matlab-mcp-tools](https://github.com/neuromechanist/matlab-mcp-tools) (Claude Code drives MATLAB).

Students are welcome to bring their own research projects and apply the same workflow in parallel. The scaffolding transfers: structured problem definition, epic/phase decomposition, plan mode, pull request review.

!!! tip "Practicum repository"
    Starter materials (the structured problem brief and the shot-events table) live at [sessions/week-03/practicum/](https://github.com/OpenScience-Collective/agentic-research-course/tree/main/sessions/week-03/practicum) in the course repo. The practicum itself is built live during the Week 3 session at [OpenScience-Collective/agentic-research-practicum](https://github.com/OpenScience-Collective/agentic-research-practicum).

## Instructor

**Seyed Yahya Shirazi, Ph.D.**
Assistant Project Scientist, Swartz Center for Computational Neuroscience, UC San Diego

- [Website](https://neuromechanist.github.io)
- [GitHub](https://github.com/neuromechanist)
- [LinkedIn](https://www.linkedin.com/in/neuromechanist/)
