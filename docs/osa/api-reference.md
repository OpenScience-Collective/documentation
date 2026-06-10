# API Reference

The OSA REST API provides programmatic access to the assistant.

## Base URL

- **Production**: `https://api.osc.earth/osa`
- **Development**: `https://api.osc.earth/osa-dev`
- **Local**: `http://localhost:38528`

## Authentication

OSA supports two authentication modes:

### Server API Key

For server-to-server access using an admin key:

```bash
curl -H "X-API-Key: your-server-key" https://api.osc.earth/osa/health
```

### BYOK (Bring Your Own Key)

Pass your OpenRouter API key directly. This is the primary method for CLI and widget users:

```bash
curl -H "X-OpenRouter-Key: your-openrouter-key" \
  https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is HED?"}'
```

When using BYOK, no server API key is required. The user's key is forwarded to the LLM provider.

## Endpoints

### Health Check

Check if the API is running.

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.7.0",
  "environment": "production"
}
```

### List Communities

Get all available communities and their widget configuration.

```
GET /communities
```

Response:
```json
[
  {
    "id": "hed",
    "name": "HED (Hierarchical Event Descriptors)",
    "description": "Event annotation standard for neuroimaging research",
    "status": "available",
    "widget": {
      "title": "HED Assistant",
      "initial_message": "Hi! I'm the HED Assistant...",
      "placeholder": "Ask about HED...",
      "suggested_questions": [
        "What is HED and how is it used?",
        "How do I annotate an event with HED tags?"
      ],
      "logo_url": "/hed/logo",
      "theme_color": "#1a365d"
    },
    "links": {
      "homepage": "https://www.hedtags.org",
      "documentation": "https://www.hed-resources.org",
      "repository": "https://github.com/hed-standard"
    }
  }
]
```

The `logo_url` field is auto-populated when a `logo.*` file exists in the community folder, or can be set explicitly in the YAML config. The `theme_color` field is only present when configured. The `links` field is `null` when no links are configured.

This endpoint is public (no authentication required).

### Community Logo

Serve the community's logo image file.

```
GET /{community}/logo
```

Returns the logo file with appropriate `Content-Type` header. Supported formats: SVG, PNG, JPG, JPEG, WEBP. SVG files include a `Content-Security-Policy` header (`default-src 'none'; style-src 'unsafe-inline'`) to prevent XSS. Responses are cached for 24 hours (`Cache-Control: public, max-age=86400`).

Returns `404` if no logo file exists for the community.

This endpoint is public (no authentication required).

### Ask

Ask a single question to a community assistant.

```
POST /{community}/ask
Content-Type: application/json
X-OpenRouter-Key: your-key

{
  "question": "How do I annotate a button press in HED?",
  "stream": true
}
```

#### Non-streaming Response

When `stream: false`:

```json
{
  "answer": "To annotate a button press in HED...",
  "tool_calls": []
}
```

#### Streaming Response (SSE)

When `stream: true` (default):

```
data: {"event": "content", "content": "To"}

data: {"event": "content", "content": " annotate"}

data: {"event": "tool_start", "name": "retrieve_hed_docs", "params": {...}}

data: {"event": "tool_end", "name": "retrieve_hed_docs", "result": "..."}

data: {"event": "content", "content": "..."}

data: {"event": "done"}
```

### Chat

Multi-turn chat with conversation history.

```
POST /{community}/chat
Content-Type: application/json
X-OpenRouter-Key: your-key

{
  "message": "How do I annotate a button press in HED?",
  "session_id": "optional-session-id",
  "stream": true
}
```

#### Non-streaming Response

```json
{
  "session_id": "abc123",
  "message": {
    "role": "assistant",
    "content": "To annotate a button press..."
  },
  "tool_calls": []
}
```

#### Streaming Response (SSE)

```
data: {"event": "session", "session_id": "abc123"}

data: {"event": "content", "content": "To"}

data: {"event": "tool_start", "name": "retrieve_hed_docs"}

data: {"event": "content", "content": " annotate"}

data: {"event": "done", "session_id": "abc123"}
```

### Mirrors

Ephemeral database mirror management. See [Database Mirrors](mirrors.md) for full documentation.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/mirrors` | Create a mirror |
| `GET` | `/mirrors` | List active mirrors |
| `GET` | `/mirrors/{id}` | Get mirror metadata |
| `DELETE` | `/mirrors/{id}` | Delete a mirror |
| `POST` | `/mirrors/{id}/refresh` | Re-copy from production |
| `POST` | `/mirrors/{id}/sync` | Run sync pipeline |
| `GET` | `/mirrors/{id}/download/{community}` | Download SQLite file |

## Public Data Feeds

Communities can expose two **read-only, unauthenticated** JSON feeds for building
their own frontends (dashboards, widgets, citation badges). Both are **opt-in per
community** via the `public_feeds` config block and return **404** when the feed is
not enabled. Responses are cacheable (`Cache-Control: public, max-age=3600`).

Currently enabled: **EEGLAB** (FAQ + citations) and **BIDS** (citations).

### FAQ Feed

Synthesized question/answer entries generated from a community's mailing-list and
forum archives.

```
GET /{community}/faq
```

No authentication required. Returns **404** if `public_feeds.faq` is not enabled.

Query parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | – | Full-text search phrase. Omit to browse all entries. |
| `category` | string | – | Filter by category (`how-to`, `troubleshooting`, `reference`, `bug-report`, `feature-request`, `discussion`). |
| `min_quality` | float | `0.0` | Minimum quality score (0.0–1.0). |
| `limit` | int | `50` | Page size (1–200). |
| `offset` | int | `0` | Pagination offset (ignored when `q` is set). |

Response:

```json
{
  "community_id": "eeglab",
  "total": 1990,
  "limit": 50,
  "offset": 0,
  "entries": [
    {
      "question": "How do I run ICA in EEGLAB?",
      "answer": "Use runica from the Tools menu...",
      "tags": ["ica", "preprocessing"],
      "category": "how-to",
      "quality_score": 0.95,
      "message_count": 4,
      "first_message_date": "2020-03-11",
      "thread_url": "https://sccn.ucsd.edu/pipermail/eeglablist/..."
    }
  ]
}
```

`total` is the count of entries matching the filters (before pagination). Email
addresses are redacted from `question`, `answer`, and `tags`.

```bash
# Browse the highest-quality how-to entries
curl "https://api.osc.earth/osa/eeglab/faq?category=how-to&min_quality=0.8&limit=10"

# Search
curl "https://api.osc.earth/osa/eeglab/faq?q=ICA%20components"
```

### Citations Feed

Per-year citation counts for a community's canonical papers, suitable for a stacked
"citations per year" chart. Counts come from OpenAlex (complete and uncapped); a
paper's preprint and published versions are merged and deduplicated, and counts are
floored at the paper's earliest publication year.

```
GET /{community}/citations
```

No authentication required. Returns **404** if `public_feeds.citations` is not
enabled. Takes no query parameters.

Response:

```json
{
  "community_id": "bids",
  "total": 3098,
  "per_year": { "2016": 22, "2017": 48, "...": 0, "2025": 502 },
  "by_paper": {
    "10.1038/sdata.2016.44": { "2016": 22, "2017": 48, "...": 0 },
    "10.1038/s41597-019-0104-8": { "2019": 12, "...": 0 }
  },
  "canonical_dois": ["10.1038/sdata.2016.44", "10.1038/s41597-019-0104-8"],
  "labels": {
    "10.1038/sdata.2016.44": "BIDS (Gorgolewski 2016)",
    "10.1038/s41597-019-0104-8": "EEG-BIDS (Pernet 2019)"
  }
}
```

| Field | Description |
|-------|-------------|
| `total` | Total citing works across all canonical papers. |
| `per_year` | Citing-work count per publication year, summed across papers. |
| `by_paper` | Stacked breakdown: canonical DOI → year → count. |
| `canonical_dois` | The DOIs tracked for this community (config order). |
| `labels` | Human-readable label per DOI for chart legends (when configured). |

```bash
curl "https://api.osc.earth/osa/bids/citations"
```

```python
import httpx

data = httpx.get("https://api.osc.earth/osa/bids/citations").json()
years = sorted(data["per_year"])
for doi, by_year in data["by_paper"].items():
    label = data["labels"].get(doi, doi)
    series = [by_year.get(y, 0) for y in years]
    print(label, series)
```

## Request Parameters

### Ask Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | Question to ask |
| `stream` | boolean | No | Enable SSE streaming (default: true) |
| `model` | string | No | Custom LLM model (requires BYOK) |

### Chat Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User message |
| `session_id` | string | No | Session ID for multi-turn chat |
| `stream` | boolean | No | Enable SSE streaming (default: true) |
| `model` | string | No | Custom LLM model (requires BYOK) |

## Headers

| Header | Description | Required |
|--------|-------------|----------|
| `X-OpenRouter-Key` | OpenRouter API key (BYOK) | Yes (or X-API-Key) |
| `X-API-Key` | Server admin API key | Yes (or BYOK) |
| `X-User-ID` | User ID for cache optimization | No |
| `X-Mirror-ID` | Route to an ephemeral database mirror (see [Database Mirrors](mirrors.md)) | No |
| `Content-Type` | Must be `application/json` | Yes |

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "API key required (or provide your own LLM key via BYOK headers)"
}
```

### 403 Forbidden

```json
{
  "detail": "Invalid API key"
}
```

### 500 Internal Server Error

```json
{
  "detail": "LLM provider error"
}
```

## Python Client Example

```python
import httpx

# Non-streaming
response = httpx.post(
    "https://api.osc.earth/osa/hed/ask",
    json={"question": "What is HED?", "stream": False},
    headers={"X-OpenRouter-Key": "your-key"},
)
print(response.json()["answer"])
```

```python
import json
import httpx

# Streaming
with httpx.Client() as client:
    with client.stream(
        "POST",
        "https://api.osc.earth/osa/hed/ask",
        json={"question": "What is HED?", "stream": True},
        headers={"X-OpenRouter-Key": "your-key"},
    ) as response:
        for line in response.iter_lines():
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if data["event"] == "content":
                    print(data["content"], end="", flush=True)
```

## cURL Examples

### Ask (Non-streaming)

```bash
curl -X POST https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"question": "What is HED?", "stream": false}'
```

### Ask (Streaming)

```bash
curl -N -X POST https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"question": "What is HED?"}'
```

### Chat with Session

```bash
curl -X POST https://api.osc.earth/osa/hed/chat \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"message": "What is HED?", "stream": false}'

# Continue conversation with session_id from response
curl -X POST https://api.osc.earth/osa/hed/chat \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"message": "Tell me more", "session_id": "abc123", "stream": false}'
```
