# Knowledge Sync

OSA includes a knowledge discovery system that syncs community-specific content from multiple sources. Each community gets its own SQLite Full-Text Search 5 (FTS5) database at `data/knowledge/{community_id}.db`, populated by sync commands.

## Overview

The knowledge system supports six sync types:

| Sync Type | Source | Description |
|-----------|--------|-------------|
| **GitHub** | GitHub REST API | Issues and Pull Requests (PRs) from community repositories |
| **Papers** | OpenALEX, Semantic Scholar, PubMed | Academic papers and citation tracking |
| **Docstrings** | GitHub repos | MATLAB/Python function documentation |
| **Mailman** | Mailman archives | Mailing list messages |
| **FAQ** | Large Language Model (LLM) summarization | Frequently Asked Questions (FAQ) entries generated from mailing list threads |
| **BEPs** | bids-website + GitHub PRs | BIDS Extension Proposals (BIDS community only) |

!!! note "Discovery, Not Answers"
    The knowledge system is for **discovery only**. The assistant links users to relevant discussions ("There's a related issue: [link]") rather than answering from them.

## Quick Start

```bash
# Initialize database for a community
uv run osa sync init --community hed

# Initialize databases for all communities
uv run osa sync init

# Sync GitHub issues/PRs
uv run osa sync github --community hed

# Sync academic papers (includes citation tracking)
uv run osa sync papers --community bids

# Sync everything for a community
uv run osa sync all --community eeglab

# Sync everything for all communities
uv run osa sync all

# Check sync status
uv run osa sync status
```

## CLI Commands

All sync commands accept `--community/-c` to specify the target community. Most default to `hed` if omitted.

### `osa sync init`

Initialize the knowledge database with FTS5 full-text search support.

```bash
# Initialize for a specific community
uv run osa sync init --community bids

# Initialize for all communities
uv run osa sync init
```

### `osa sync github`

Sync GitHub issues and PRs from community repositories.

```bash
# Sync all repos for a community
uv run osa sync github --community hed

# Sync a specific repo
uv run osa sync github --community hed -r hed-standard/hed-specification

# Full sync (not incremental)
uv run osa sync github --community bids --full
```

**Options:**

| Option | Description |
|--------|-------------|
| `-c, --community` | Community ID (default: `hed`) |
| `-r, --repo` | Specific repository to sync |
| `--full` | Full sync instead of incremental |

Repositories are configured per-community in `config.yaml` under `github.repos`.

### `osa sync papers`

Sync academic papers from multiple sources.

```bash
# Sync papers for a community (includes citations by default)
uv run osa sync papers --community bids

# Sync from a specific source
uv run osa sync papers --community hed -s openalex

# Custom search query
uv run osa sync papers --community hed -q "event annotation EEG"

# Disable citation tracking
uv run osa sync papers --community hed --no-citations
```

**Options:**

| Option | Description |
|--------|-------------|
| `-c, --community` | Community ID (default: `hed`) |
| `-s, --source` | Paper source: `openalex`, `semanticscholar`, `pubmed` |
| `-q, --query` | Custom search query (overrides community config) |
| `-l, --limit` | Max papers per query (default: `100`) |
| `--citations / --no-citations` | Sync papers citing community DOIs (default: enabled) |

!!! info "Citation Tracking"
    When `--citations` is enabled (the default), OSA also syncs papers that cite the DOIs listed in the community's `citations.dois` config. This automatically discovers new research that builds on the community's core publications.

!!! info "Automatic Deduplication"
    Papers are deduplicated using fuzzy title matching. The same paper from different sources is only shown once in search results.

### `osa sync docstrings`

Sync code docstrings from GitHub repositories. Extracts documentation from MATLAB (`.m`) or Python (`.py`) files and indexes them for search.

```bash
# Sync all configured repos for a community
uv run osa sync docstrings --community eeglab --language matlab

# Sync Python docstrings
uv run osa sync docstrings --community eeglab --language python

# Sync a specific repo
uv run osa sync docstrings --community eeglab -r sccn/eeglab -b develop
```

**Options:**

| Option | Description |
|--------|-------------|
| `-c, --community` | Community ID (default: `hed`) |
| `-l, --language` | Language: `matlab` or `python` (default: `matlab`) |
| `-r, --repo` | Single repo to sync (`owner/name` format) |
| `-b, --branch` | Branch to sync from (default: `main`) |

Repositories and their branches are configured in `config.yaml` under `docstrings.repos`.

### `osa sync mailman`

Sync mailing list messages from Mailman archives.

```bash
# Sync all configured mailing lists for a community
uv run osa sync mailman --community eeglab

# Sync a specific mailing list
uv run osa sync mailman --community eeglab --list eeglablist

# Sync a specific year range
uv run osa sync mailman --community eeglab --start-year 2020 --end-year 2025
```

**Options:**

| Option | Description |
|--------|-------------|
| `-c, --community` | Community ID (default: `eeglab`) |
| `--list` | Specific mailing list name |
| `--start-year` | Earliest year to sync |
| `--end-year` | Latest year to sync |

Mailing lists are configured in `config.yaml` under `mailman`.

### `osa sync faq`

Generate FAQ summaries from mailing list threads using a two-stage LLM pipeline.

```bash
# Estimate cost first
uv run osa sync faq --community eeglab --estimate

# Generate FAQs with quality threshold
uv run osa sync faq --community eeglab --quality 0.7

# Limit number of threads to process
uv run osa sync faq --community eeglab --max 100
```

**Options:**

| Option | Description |
|--------|-------------|
| `-c, --community` | Community ID (default: `eeglab`) |
| `--estimate` | Estimate cost without processing |
| `--quality` | Minimum quality score, 0.0-1.0 (default: `0.6`) |
| `--max` | Maximum threads to process |

!!! warning "LLM Costs"
    FAQ generation uses LLM calls. Always run with `--estimate` first to understand costs. The two-agent pipeline (evaluation + summarization) reduces costs by filtering low-quality threads early.

### `osa sync beps`

Sync BIDS Extension Proposals (BEPs) from the BIDS website and specification PRs.

```bash
uv run osa sync beps --community bids
```

**Options:**

| Option | Description |
|--------|-------------|
| `-c, --community` | Community ID (default: `bids`) |

### `osa sync all`

Sync all knowledge sources for one or all communities. Runs GitHub, papers, and BEPs (for BIDS) in sequence.

```bash
# Sync everything for one community
uv run osa sync all --community hed

# Sync everything for all communities
uv run osa sync all

# Full non-incremental sync
uv run osa sync all --community bids --full
```

### `osa sync status`

Show sync status and database statistics. This is a read-only command and does not require API keys.

```bash
# Show status for all communities
uv run osa sync status

# Show status for a specific community
uv run osa sync status --community bids
```

### `osa sync search`

Search the knowledge database (useful for testing).

```bash
# Search a community's knowledge base
uv run osa sync search "validation error" --community hed

# Filter by source
uv run osa sync search "ICA" --community eeglab --source github
```

## Automated Sync

When running OSA in production, each community has its own sync schedule configured in its `config.yaml` under the `sync` key. Schedules use APScheduler cron expressions (UTC timezone).

**Example from EEGLAB config:**

```yaml
sync:
  github:
    cron: "0 2 * * *"       # daily at 2am UTC
  papers:
    cron: "0 3 * * 0"       # weekly Sunday at 3am UTC
  docstrings:
    cron: "0 4 * * 1"       # weekly Monday at 4am UTC
  mailman:
    cron: "0 5 * * 1"       # weekly Monday at 5am UTC
  faq:
    cron: "0 6 1 * *"       # monthly 1st at 6am UTC
```

Not all sync types are required. A community only needs schedules for the sync types it uses.

## Database Location

Each community has its own SQLite database:

| Environment | Location |
|-------------|----------|
| Local (macOS) | `~/Library/Application Support/osa/knowledge/{community_id}.db` |
| Local (Linux) | `~/.local/share/osa/knowledge/{community_id}.db` |
| Docker | `/app/data/knowledge/{community_id}.db` |

The location can be overridden with the `DATA_DIR` environment variable.

## API Keys

All API keys are optional but recommended for higher rate limits:

| API Key | Purpose | Required For |
|---------|---------|-------------|
| `GITHUB_TOKEN` | GitHub API (issues/PRs) | `sync github` |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API | `sync papers -s semanticscholar` |
| `PUBMED_API_KEY` | PubMed/NCBI API | `sync papers -s pubmed` |
| `OPENALEX_EMAIL` | OpenALEX polite pool | `sync papers -s openalex` |

!!! note
    `sync status` and `sync search` are read-only and do not require API keys.

Without keys, rate limits apply:

- GitHub: 60 requests/hour
- Semantic Scholar: ~100 requests/5 minutes
- PubMed: 3 requests/second

## Agent Tools

Each community's assistant gets knowledge discovery tools based on its configuration:

| Tool | Description | Config Requirement |
|------|-------------|-------------------|
| `search_{community}_discussions` | Search GitHub issues and PRs | `github.repos` |
| `list_{community}_recent` | List recent GitHub activity | `github.repos` |
| `search_{community}_papers` | Search academic papers | `citations` |
| `search_{community}_code_docs` | Search code docstrings | `docstrings` |
| `search_{community}_faq` | Search mailing list FAQ | `mailman` + `faq_generation` |

See the [Tools](tools/index.md) section for detailed tool documentation per community.

## Troubleshooting

### Rate limiting

If you hit rate limits, configure API keys in your `.env` file. See the API Keys section above.

### Database corruption

If the database becomes corrupted, delete and reinitialize:

```bash
# Find the database location
uv run osa sync status --community hed

# Delete and reinitialize
rm ~/.local/share/osa/knowledge/hed.db
uv run osa sync init --community hed
uv run osa sync all --community hed
```

### Sync shows 0 items

- Check that the community's `config.yaml` has the relevant configuration (e.g., `github.repos` for GitHub sync)
- Ensure API keys are set if required
- Run with `--full` to bypass incremental sync
