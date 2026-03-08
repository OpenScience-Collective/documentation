# Database Mirrors

Ephemeral database mirrors let developers work on isolated copies of community knowledge databases without running a local server. Instead of full ephemeral backends (Docker containers, port allocation, proxies), mirrors provide lightweight SQLite copies that can be created and destroyed in seconds.

## How it Works

```
Developer's CLI                     OSA Backend
┌──────────────┐                   ┌────────────────────────┐
│ osa ask      │  X-Mirror-ID     │                        │
│ --mirror     │  ──────────────> │  Middleware sets        │
│   abc123     │                  │  ContextVar             │
│              │                  │     │                   │
│              │                  │     v                   │
│              │                  │  get_db_path("hed")     │
│              │                  │  returns:               │
│              │                  │  mirrors/abc123/hed.db  │
│              │                  │  (instead of            │
│              │                  │   knowledge/hed.db)     │
└──────────────┘                  └────────────────────────┘
```

One shared backend, many lightweight database copies. All search, sync, and tool code works unmodified because every database access flows through a single function (`get_db_path`) that checks a `ContextVar`.

## Quick Start

```bash
# Create a mirror of the HED and BIDS databases
osa mirror create -c hed -c bids --label "testing-new-prompt"

# Use with: osa ask "question" -a hed --mirror abc123def456
# Mirror created: abc123def456

# Ask questions against your mirror
osa ask -a hed "How do I annotate a button press?" --mirror abc123def456

# Interactive chat with your mirror
osa chat -a hed --mirror abc123def456

# Re-sync from public sources into your mirror
osa mirror sync abc123def456 --type github

# When done, clean up
osa mirror delete abc123def456
```

## What Works vs. What Doesn't

### Works with mirrors (no local server needed)

- Querying existing community databases with different data
- Re-syncing from public sources (GitHub, papers, etc.) into mirror
- Using BYOK with any LLM provider
- Multiple developers working independently
- Testing retrieval quality with modified data

### Requires a local server

- **Schema changes**: New tables/columns need new Python code
- **New community from scratch**: Server has no routes for unregistered communities
- **Modified tool/search code**: Remote server runs deployed code, not your branch
- **Modified sync pipeline**: Same; remote runs old sync logic
- **Local LLM**: LLM must be reachable from server

For these cases, use `osa mirror pull` to download mirror databases locally, then run `osa serve`:

```bash
# Download mirror databases locally
osa mirror pull abc123def456

# Run local server with the downloaded data
osa serve
```

## CLI Commands

### `osa mirror create`

Create a new ephemeral database mirror.

```bash
osa mirror create -c hed -c bids
osa mirror create -c hed --label "testing-new-prompt" --ttl 24
```

| Option | Description | Default |
|--------|-------------|---------|
| `--community, -c` | Community ID to include (repeatable) | Required |
| `--label, -l` | Human-readable label | None |
| `--ttl` | Hours until mirror expires (1-168) | 48 |
| `--api-key, -k` | OpenRouter API key | From config |
| `--api-url` | Override API URL | From config |

### `osa mirror list`

List all active mirrors.

```bash
osa mirror list
```

### `osa mirror info`

Show detailed information about a mirror.

```bash
osa mirror info abc123def456
```

### `osa mirror delete`

Delete a mirror and its databases.

```bash
osa mirror delete abc123def456
osa mirror delete abc123def456 --yes  # skip confirmation
```

### `osa mirror refresh`

Re-copy production databases into an existing mirror (resets to current production state).

```bash
osa mirror refresh abc123def456
osa mirror refresh abc123def456 -c hed  # refresh only HED
```

### `osa mirror sync`

Run sync pipeline against a mirror's databases (populates from public sources).

```bash
osa mirror sync abc123def456              # sync all types
osa mirror sync abc123def456 --type github  # sync only GitHub
```

Supported sync types: `github`, `papers`, `docstrings`, `mailman`, `faq`, `beps`, `all`.

### `osa mirror pull`

Download mirror databases locally for offline development.

```bash
osa mirror pull abc123def456
osa mirror pull abc123def456 -c hed -o ./data/knowledge
```

## API Endpoints

All mirror endpoints require authentication (BYOK or admin key).

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/mirrors` | Create a mirror |
| `GET` | `/mirrors` | List active mirrors |
| `GET` | `/mirrors/{id}` | Get mirror metadata |
| `DELETE` | `/mirrors/{id}` | Delete a mirror |
| `POST` | `/mirrors/{id}/refresh` | Re-copy from production |
| `POST` | `/mirrors/{id}/sync` | Run sync pipeline |
| `GET` | `/mirrors/{id}/download/{community}` | Download SQLite file |

### Create Mirror

```bash
curl -X POST https://api.osc.earth/osa/mirrors \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"community_ids": ["hed", "bids"], "ttl_hours": 48, "label": "my-test"}'
```

Response:

```json
{
  "mirror_id": "abc123def456",
  "community_ids": ["hed", "bids"],
  "created_at": "2026-03-07T12:00:00+00:00",
  "expires_at": "2026-03-09T12:00:00+00:00",
  "label": "my-test",
  "size_bytes": 1048576,
  "expired": false
}
```

### Query with Mirror

Include the `X-Mirror-ID` header with any existing endpoint:

```bash
curl -X POST https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -H "X-Mirror-ID: abc123def456" \
  -d '{"question": "What is HED?"}'
```

## Resource Limits

| Limit | Default |
|-------|---------|
| Max mirrors total | 50 |
| Max mirrors per BYOK user | 2 |
| Max TTL | 7 days (168 hours) |
| Default TTL | 48 hours |

Expired mirrors are automatically cleaned up by the server every hour. Admin key holders are only subject to the global mirror cap.

## Architecture

### Storage Layout

```
data/
  knowledge/           # Production databases (unchanged)
    hed.db
    bids.db
  mirrors/             # Ephemeral copies
    abc123def456/      # mirror_id
      _metadata.json   # Timestamps, label, communities
      hed.db           # Copy of production hed.db
      bids.db          # Copy of production bids.db
```

### ContextVar Routing

All database access flows through `get_db_path(project)` in `src/knowledge/db.py`. When a mirror is active:

1. Request arrives with `X-Mirror-ID: abc123` header
2. Middleware validates the mirror exists and isn't expired
3. Middleware sets a `contextvars.ContextVar` for the request
4. `get_db_path("hed")` returns `data/mirrors/abc123/hed.db` instead of `data/knowledge/hed.db`
5. All search, sync, and tool functions work unmodified
6. Middleware resets the ContextVar when the request completes

### Security

- Mirror IDs are validated against path traversal (alphanumeric, hyphens, underscores only, max 64 chars)
- Community IDs are validated at the API boundary
- Per-user rate limits prevent resource exhaustion
- Expired mirrors return HTTP 410 Gone
- Auto-cleanup runs hourly
