# Knowledge Sync

OSA includes a knowledge discovery system that syncs GitHub discussions and academic papers for HED-related content. This helps the assistant link users to relevant discussions and research, not as authoritative knowledge sources, but for discovery.

## Overview

The knowledge database stores:

- **GitHub Issues and PRs** from HED repositories (hed-specification, hed-schemas, hed-javascript)
- **Academic Papers** from OpenALEX, Semantic Scholar, and PubMed

!!! note "Discovery, Not Answers"
    The knowledge system is for **discovery only**. The assistant links users to relevant discussions ("There's a related issue: [link]") rather than answering from them.

## Quick Start

```bash
# Initialize the database
uv run osa sync init

# Sync GitHub issues/PRs
uv run osa sync github

# Sync academic papers
uv run osa sync papers

# Sync everything
uv run osa sync all

# Check sync status
uv run osa sync status
```

## CLI Commands

### `osa sync init`

Initialize the knowledge database. Creates the SQLite database with FTS5 full-text search support.

```bash
uv run osa sync init
```

### `osa sync github`

Sync GitHub issues and PRs from HED repositories.

```bash
# Sync all HED repos
uv run osa sync github

# Sync specific repo
uv run osa sync github -r hed-standard/hed-specification
```

Options:

- `-r, --repo`: Specific repository to sync (e.g., `hed-standard/hed-specification`)

**Synced repositories:**

- `hed-standard/hed-specification`
- `hed-standard/hed-schemas`
- `hed-standard/hed-javascript`

### `osa sync papers`

Sync academic papers from multiple sources.

```bash
# Sync from all sources
uv run osa sync papers

# Sync from specific source
uv run osa sync papers -s openalex
uv run osa sync papers -s semanticscholar
uv run osa sync papers -s pubmed

# Custom search query
uv run osa sync papers -q "BIDS event annotation"
```

Options:

- `-s, --source`: Paper source (`openalex`, `semanticscholar`, `pubmed`)
- `-q, --query`: Custom search query (default: "HED annotation" OR "Hierarchical Event Descriptors")

### `osa sync all`

Sync all knowledge sources (GitHub + papers).

```bash
uv run osa sync all
```

### `osa sync status`

Show sync status and database statistics.

```bash
uv run osa sync status
```

Example output:

```
Knowledge Database Status
─────────────────────────
Database: ~/.local/share/osa/knowledge/hed.db

GitHub Items:
  hed-standard/hed-specification: 45 issues, 23 PRs
  hed-standard/hed-schemas: 12 issues, 8 PRs
  hed-standard/hed-javascript: 18 issues, 5 PRs
  Last sync: 2026-01-12 02:00:00 UTC

Papers:
  OpenALEX: 42 papers
  Semantic Scholar: 38 papers
  PubMed: 25 papers
  Last sync: 2026-01-05 03:00:00 UTC
```

### `osa sync search`

Search the knowledge database (for testing).

```bash
uv run osa sync search "validation error"
```

## Automated Sync (Docker)

When running OSA in Docker, the scheduler automatically syncs knowledge sources:

| Source | Default Schedule | Environment Variable |
|--------|-----------------|---------------------|
| GitHub | Daily at 2am UTC | `SYNC_GITHUB_CRON` |
| Papers | Weekly Sunday 3am UTC | `SYNC_PAPERS_CRON` |

### Configuration

Configure via environment variables in your `.env` file:

```bash
# Enable/disable automated sync
SYNC_ENABLED=true

# Sync schedules (cron expressions, UTC timezone)
SYNC_GITHUB_CRON=0 2 * * *      # Daily at 2am
SYNC_PAPERS_CRON=0 3 * * 0      # Weekly Sunday at 3am

# Optional API keys for higher rate limits
GITHUB_TOKEN=ghp_...
SEMANTIC_SCHOLAR_API_KEY=...
PUBMED_API_KEY=...
```

### Docker Compose

The included `docker-compose.yml` mounts a volume for database persistence:

```yaml
services:
  osa:
    volumes:
      - osa-data:/app/data

volumes:
  osa-data:
```

This ensures the knowledge database persists across container restarts.

## Manual Sync Trigger

You can manually trigger sync at any time:

```bash
# Inside Docker container
docker exec osa uv run osa sync all

# Or from host with CLI
uv run osa sync all
```

## Database Location

| Environment | Location |
|-------------|----------|
| Local (macOS) | `~/Library/Application Support/osa/knowledge/hed.db` |
| Local (Linux) | `~/.local/share/osa/knowledge/hed.db` |
| Docker | `/app/data/knowledge/hed.db` |

The location can be overridden with the `DATA_DIR` environment variable.

## API Keys

All API keys are optional but recommended for higher rate limits:

| API Key | Purpose | Get Key |
|---------|---------|---------|
| `GITHUB_TOKEN` | GitHub API (issues/PRs) | [GitHub Settings](https://github.com/settings/tokens) |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API | [S2 API](https://www.semanticscholar.org/product/api) |
| `PUBMED_API_KEY` | PubMed/NCBI API | [NCBI Settings](https://www.ncbi.nlm.nih.gov/account/settings/) |

## Agent Tools

The HED assistant has access to knowledge discovery tools:

### `search_hed_discussions`

Search GitHub issues and PRs for related discussions.

```
"Can you find any discussions about validation errors?"
→ "There's a related discussion in hed-specification#123: [link]"
```

### `search_hed_papers`

Search academic papers related to HED.

```
"Are there papers about HED in neuroimaging?"
→ "I found a relevant paper: 'HED Annotation Best Practices' [link]"
```

## Troubleshooting

### Sync fails with "gh: command not found"

The `gh` CLI is required for GitHub sync. Install it:

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh
```

### Rate limiting

If you hit rate limits, configure API keys in your `.env` file. Without keys:

- GitHub: 60 requests/hour
- Semantic Scholar: ~100 requests/5 minutes
- PubMed: 3 requests/second

With keys, limits are significantly higher.

### Database corruption

If the database becomes corrupted, delete and reinitialize:

```bash
rm ~/.local/share/osa/knowledge/hed.db
uv run osa sync init
uv run osa sync all
```
