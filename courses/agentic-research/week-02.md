# Week 2: Setting Up Claude Code for Research

## Overview

Last week we installed the safety net: git, GitHub, and the terminal. This week we install the tool that makes the safety net necessary. Claude Code is an AI coding agent that reads your entire project, writes code across multiple files, runs commands, creates pull requests, and iterates on its own work. Setting it up correctly, and giving it the right instructions through a project-level `CLAUDE.md` file, is what turns a generic AI into a domain-aware research assistant.

The session is structured around one key insight from Anthropic's own documentation: Claude Code is only as good as the context you give it. A well-written `CLAUDE.md` plus the right ecosystem of skills, hooks, and MCP servers is the difference between an AI that guesses and an AI that knows your project.

!!! abstract "Learning Objectives"
    - Install Claude Code on macOS, Linux, or Windows and authenticate
    - Understand the permission model: Default, Accept Edits, Plan, and Auto modes
    - Write an effective `CLAUDE.md` with project context, workflow rules, and never-do lists
    - Use Plan Mode (Shift+Tab) to explore before implementing
    - Distinguish between plugins, skills, MCP servers, hooks, and subagents, and know when to reach for each
    - Apply Anthropic's three core best practices: verify, explore-then-plan-then-code, manage context aggressively
    - Set up the `.context/` directory pattern for tracking project state across sessions
    - Identify the nonprofit pricing option available to 501(c)(3) university labs

<div class="embed-container">
  <iframe
    src="https://www.youtube.com/embed/PLACEHOLDER"
    title="Week 2: Setting Up Claude Code for Research"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>

## Slides

<div class="embed-container">
  <iframe
    src="../../slides/agentic-research/week-02/presentation.html?presentation=./week-02.json"
    title="Week 2 Slides"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>

<p class="slide-hint">Use arrow keys to navigate. Press <kbd>F</kbd> for fullscreen, <kbd>?</kbd> for shortcuts.</p>

---

## Setup Guide

A step-by-step walkthrough for installing Claude Code and writing your first `CLAUDE.md`. No prior AI tooling experience is assumed.

### 1. Understand What Claude Code Is

Claude Code is not autocomplete, and it is not a chat sidebar. It is an agent that:

- Reads your entire project and understands the structure
- Writes and edits code across multiple files
- Runs terminal commands (build, test, lint, deploy)
- Creates git commits, branches, and pull requests
- Plans multi-step implementations before writing code
- Iterates on its own work until tests pass

You describe the outcome you want. Claude Code figures out how to build it.

!!! info "Claude Code vs Claude Chat vs Claude Cowork"
    Anthropic offers three agentic products. Claude Chat is the conversational AI you already know. Claude Code is what this course is about: an agent for developers and researchers. Claude Cowork is the newest (generally available in April 2026), aimed at non-coding knowledge workers who want Claude to build spreadsheets, slide decks, and documents. All three are available on Pro and above.

### 2. Install Claude Code

=== "macOS"

    Native install (recommended, auto-updates):

    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    Or via Homebrew:

    ```bash
    brew install --cask claude-code
    ```

=== "Linux"

    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

=== "Windows"

    In PowerShell:

    ```powershell
    irm https://claude.ai/install.ps1 | iex
    ```

    Native Windows installs require [Git for Windows](https://git-scm.com/downloads/win). WSL setups do not.

Verify the install:

```bash
claude --version
```

### 3. First Run and Authentication

```bash
cd your-project
claude
```

On first run, a browser window opens for login. You can sign in with a Claude subscription (Pro, Max, Team, or Enterprise) or with an Anthropic Console account for pay-per-token access.

Check your auth state at any time:

```bash
claude auth status
```

!!! tip "Which plan for this course?"
    **Pro at $20/month** (or $17/month with annual billing) is sufficient for everything we do. Max gives you 5x or 20x the usage if you run out of quota frequently.

    PIs: if your lab has fewer than 20 people at a 501(c)(3) university, apply as the nonprofit purchasing unit for the Team plan at $8 per seat per month through Goodstack. See [Anthropic's nonprofits page](https://claude.com/solutions/nonprofits) for details.

### 4. The Permission Model

Claude Code asks before doing anything destructive. You control the guardrails through four modes:

| Mode | Behavior | When to use |
|------|----------|-------------|
| **Default** | Asks before edits and shell commands | Starting out |
| **Accept Edits** | Auto-approves file edits plus common filesystem commands (`mkdir`, `mv`, `cp`, `rm`, `sed`) | Trusted coding sessions |
| **Plan** | Prevents edits; Claude can still read and run commands with prompts | Complex multi-file changes |
| **Auto** | A safety classifier evaluates each action | Team/Enterprise/API only; opt-in via `--enable-auto-mode` |

Press `Shift+Tab` in any session to cycle Default, Accept Edits, Plan. Auto mode is not in the default cycle and is not available on Pro or Max.

Use `/permissions` to persist allow/deny rules across sessions. See [the permissions doc](https://code.claude.com/docs/en/permissions) for advanced patterns.

### 5. Write Your First `CLAUDE.md`

`CLAUDE.md` is a plain markdown file at your project root. Claude Code reads it at the start of every session. This is the most important file in your project for AI-assisted development.

Let Claude Code bootstrap it for you:

```bash
cd your-project
claude
```

Then at the prompt:

```
/init
```

Claude analyzes your codebase and generates a starting `CLAUDE.md` with build commands, test instructions, and conventions it discovers. Refine it manually from there.

**What to include:**

- Build, test, and lint commands Claude cannot guess
- Code style rules that differ from defaults
- Repository etiquette (branch naming, PR conventions, commit style)
- Architecture decisions specific to your project
- Common gotchas or non-obvious behaviors
- A "never do this" section for hard rules

**What to exclude:**

- Anything Claude can figure out by reading your code
- Standard language conventions Claude already knows
- Detailed API documentation (link to it instead)
- Information that changes frequently
- Self-evident practices like "write clean code"

!!! warning "Keep it under 200 lines"
    The single most common mistake is a bloated `CLAUDE.md`. Long files cause Claude to ignore rules because important instructions get buried. If you see Claude already doing something correctly without the rule, delete the rule. Prune regularly; treat it like code.

**Scope hierarchy** (most specific wins):

| Scope | Location | Shared with |
|-------|----------|-------------|
| Organization | System-level, IT-deployed | All users on the machine |
| Project | `./CLAUDE.md` (in repo) | Team, via git |
| User | `~/.claude/CLAUDE.md` | Just you, all projects |
| Local | `./CLAUDE.local.md` (gitignored) | Just you, this project |

All four are concatenated into context. Within each directory, the local file appends after the project file, so your personal notes take precedence at that level.

### 6. Structure Project State with `.context/`

`CLAUDE.md` holds static rules. Claude also needs to know what you are working on right now, what you already tried, and what decisions led here. The `.context/` directory is a pattern we use across our projects for tracking this evolving state:

```
your-project/
├── CLAUDE.md
└── .context/
    ├── plan.md              # Current tasks, phases, status
    ├── ideas.md             # Design decisions, architecture notes
    ├── research.md          # Technical findings, solutions considered
    └── scratch_history.md   # Failed attempts, lessons learned
```

Claude reads these files alongside `CLAUDE.md`. Your `plan.md` becomes its task list. Your `scratch_history.md` prevents it from repeating your mistakes. This pattern is not an official Claude Code feature; it is an opinionated workflow we have found most useful in research codebases.

You can scaffold the directory manually, or use the `project` plugin from [research-skills](https://github.com/neuromechanist/research-skills):

```bash
claude plugin install project@research-skills
/init-project
```

### 7. Plan Mode: Think Before You Code

The single highest-impact feature for research workflows is Plan Mode. Press `Shift+Tab` twice to enter it.

1. **Explore** (Plan Mode): Claude reads files, asks questions, builds understanding. It cannot edit anything.
2. **Plan** (Plan Mode): Claude proposes an implementation plan. Press `Ctrl+G` to open the plan in your text editor and revise it.
3. **Implement** (Normal Mode): Shift+Tab back to Default or Accept Edits. Claude follows the approved plan.
4. **Commit** (Normal Mode): Claude writes the commit message and opens a PR.

Use Plan Mode when:

- The change spans multiple files
- You are unfamiliar with the code being modified
- You are not certain of the approach

Skip Plan Mode for small, obvious edits (fixing a typo, adding a log line, renaming a variable). Planning overhead does not pay off there.

### 8. Understand the Ecosystem

Claude Code has five extension mechanisms. Knowing when to reach for each saves a lot of time.

| Concept | What it is | When to use |
|---------|-----------|-------------|
| **Plugin** | Distributable package bundling everything below | Share tools with a team or community |
| **Skill** | Workflow or knowledge file, loads on demand | Repeatable procedures and checklists |
| **MCP server** | Connector to external data or tools | Google Drive, Jira, databases, MATLAB, HED |
| **Hook** | Automated shell command at a lifecycle point | Enforce something with zero exceptions |
| **Subagent** | Isolated worker with its own context window | Side tasks that would pollute main context |

Three useful distinctions:

- **Hooks say "this WILL happen."** Deterministic.
- **CLAUDE.md says "please do this."** Advisory.
- **Subagents say "do this in your own space."** Keep your main conversation clean.

For our research practicum, we use [`matlab-mcp-tools`](https://github.com/neuromechanist/matlab-mcp-tools) as an MCP server so Claude Code can drive EEGLAB for the HBN analysis. We also use [Serena](https://github.com/oraios/serena) for semantic code exploration, and LSP servers for real-time code intelligence in typed languages. For neuroimaging workflows, `hed-mcp` handles Hierarchical Event Descriptor annotation.

### 9. Apply the Three Core Best Practices

These come directly from Anthropic's [official best practices page](https://code.claude.com/docs/en/best-practices). They are the highest-leverage habits for agentic work.

!!! tip "1. Give Claude a way to verify its work"
    Include tests, expected outputs, or screenshots. This is the single highest-leverage thing you can do. Without verification, every mistake requires your attention.

    Instead of: `"add tests for foo.py"`

    Write: `"write a test for foo.py covering the edge case where the user is logged out. avoid mocks. run the test and fix any failures."`

!!! tip "2. Explore first, then plan, then code"
    Use Plan Mode to separate research from execution. This prevents solving the wrong problem when the scope is non-trivial.

!!! tip "3. Manage context aggressively"
    Claude's context window fills up fast, and performance degrades as it fills.

    - `/clear` between unrelated tasks
    - Use subagents for investigation so exploration does not consume your main context
    - After two failed corrections, `/clear` and rewrite your prompt with what you learned

### 10. Useful Commands

The commands you will reach for most:

| Command | What it does |
|---------|-------------|
| `/init` | Generate a starter `CLAUDE.md` |
| `/plan [description]` | Enter Plan Mode |
| `/clear` | Reset context between unrelated tasks |
| `/compact [focus]` | Summarize conversation to free context |
| `/memory` | Edit `CLAUDE.md`, toggle auto-memory |
| `/model` | Switch between Opus, Sonnet, Haiku |
| `/diff` | Interactive viewer of uncommitted changes |
| `/rewind` | Undo to any previous checkpoint |
| `/cost` | Show token usage |
| `/context` | Visualize context window usage |

Key shortcuts:

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle permission modes |
| `Esc` | Stop Claude mid-action |
| `Esc` twice | Open rewind menu |
| `Ctrl+G` | Open current input in your text editor |
| `@` at start | File path autocomplete |
| `!` at start | Bash mode (run commands directly) |

---

## Before Next Session

!!! note "Homework"
    - Install Claude Code: `claude --version` should work
    - Run `/init` in a real project to generate a `CLAUDE.md`
    - Create the `.context/` directory with four starter files (`plan.md`, `ideas.md`, `research.md`, `scratch_history.md`)
    - Give Claude one real task from your research; small is fine (plot some data, write a function, summarize a file)
    - Review the `CLAUDE.md` Claude generated and refine it manually based on what worked or did not
    - Optional: install the `project` plugin from [research-skills](https://github.com/neuromechanist/research-skills) to scaffold everything automatically

    Next week: project management with epics, sprints, and git worktrees.

---

## Quick Reference

### Install and first run

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Then in any project
cd your-project
claude
```

### The five extension mechanisms

| Mechanism | File location | Invoke with |
|-----------|--------------|-------------|
| Plugin | Installed via `/plugin install name@marketplace` | `/plugin-name:command` |
| Skill | `.claude/skills/<name>/SKILL.md` | `/skill-name` or Claude auto-detects |
| MCP server | `.mcp.json` or `claude mcp add` | Claude uses when relevant |
| Hook | `.claude/settings.json` | Fires automatically at lifecycle event |
| Subagent | `.claude/agents/<name>.md` | Claude delegates based on description |

### Bundled skills (ship with Claude Code)

| Command | What it does |
|---------|-------------|
| `/simplify` | Review and improve recent code |
| `/batch` | Parallelize large changes across worktrees |
| `/debug` | Enable debug logging and troubleshoot |
| `/loop` | Run a prompt repeatedly on an interval |
| `/claude-api` | Load Claude API reference for your language |

---

## Resources

- [Claude Code documentation](https://code.claude.com/docs) (official)
- [Best practices](https://code.claude.com/docs/en/best-practices) (Anthropic)
- [Memory / CLAUDE.md](https://code.claude.com/docs/en/memory)
- [Plugins](https://code.claude.com/docs/en/plugins)
- [Skills](https://code.claude.com/docs/en/skills)
- [MCP (Model Context Protocol)](https://code.claude.com/docs/en/mcp)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Nonprofit pricing](https://claude.com/solutions/nonprofits) (for 501(c)(3) labs)
- [Course repository](https://github.com/OpenScience-Collective/agentic-research-course)
- [Open Science Collective Discord](https://discord.gg/5dWJCUmUww)
- [research-skills plugin](https://github.com/neuromechanist/research-skills) (course companion)
- [matlab-mcp-tools](https://github.com/neuromechanist/matlab-mcp-tools) (EEGLAB integration for the practicum)

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
