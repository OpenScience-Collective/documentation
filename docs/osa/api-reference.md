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

Pass your own LLM key in a header, one header per provider.
This is the primary method for CLI and widget users:

```bash
# Claude Platform key
curl -H "X-Anthropic-API-Key: sk-ant-your-key" \
  https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is HED?"}'

# OpenRouter key
curl -H "X-OpenRouter-Key: sk-or-v1-your-key" \
  https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is HED?"}'
```

When using BYOK, no server API key is required. The user's key is forwarded to the LLM provider.
Send both headers and the Anthropic one is used, since it is the platform's own
provider.

Without a BYOK header, a question is answered on the community's key if it has
one, and the platform's otherwise.

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
  "version": "X.Y.Z",
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
      "documentation": "https://www.hedtags.org/hed-resources",
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
X-Anthropic-API-Key: sk-ant-your-key

{
  "question": "How do I annotate a button press in HED?",
  "stream": true,
  "model": "claude-sonnet-5"
}
```

`model` is optional: `claude-haiku-4-5` or `claude-sonnet-5`, or a legacy alias
of either. Any other id needs an OpenRouter key. Omit it to use the community's
configured default.

#### Non-streaming Response

When `stream: false` (the default for `/ask`):

```json
{
  "answer": "To annotate a button press in HED, use the Press tag [1]...",
  "tool_calls": [],
  "citations": [
    {
      "marker": 1,
      "source": "https://www.hedtags.org/hed-resources/HedAnnotationQuickstart.html",
      "title": "HED annotation quickstart",
      "cited_text": "Agent-action tags describe what a participant did..."
    }
  ],
  "request_id": "req_abc123",
  "model": "claude-haiku-4-5"
}
```

`citations` backs the `[n]` markers in the answer, in marker order.
One marker per unique source, so repeated claims from the same document share a
number. It is empty when the model cited nothing, and on the OpenRouter path,
which has no citation mechanism.
`model` is the model that actually answered, which is worth reading rather than
assuming: a cost guard or an alias may have resolved it to something other than
what was requested.

#### Streaming Response (SSE)

When `stream: true`:

```
data: {"event": "content", "content": "To"}

data: {"event": "content", "content": " annotate"}

data: {"event": "tool_start", "name": "retrieve_hed_docs", "params": {...}}

data: {"event": "tool_end", "name": "retrieve_hed_docs", "result": "..."}

data: {"event": "content", "content": " use the Press tag [1]"}

data: {"event": "citation", "marker": 1, "source": "...", "title": "...", "cited_text": "..."}

data: {"event": "done", "request_id": "...", "model": "claude-haiku-4-5", "citations": [...]}
```

A `citation` event arrives at the end of the span it annotates, right after the
`content` chunk carrying its `[n]`, so a client that ignores the event still
shows the marker in place. `done` repeats the full list, so a client that missed
an event can still render the sources.

### Chat

Multi-turn chat with conversation history.

```
POST /{community}/chat
Content-Type: application/json
X-Anthropic-API-Key: sk-ant-your-key

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
    "content": "To annotate a button press... [1]"
  },
  "tool_calls": [],
  "citations": [
    {
      "marker": 1,
      "source": "https://www.hedtags.org/hed-resources/HedAnnotationQuickstart.html",
      "title": "HED annotation quickstart",
      "cited_text": "Agent-action tags describe what a participant did..."
    }
  ],
  "request_id": "req_abc123",
  "model": "claude-haiku-4-5"
}
```

#### Streaming Response (SSE)

Streaming is the default for `/chat`.

```
data: {"event": "session", "session_id": "abc123"}

data: {"event": "content", "content": "To"}

data: {"event": "tool_start", "name": "retrieve_hed_docs"}

data: {"event": "content", "content": " annotate... [1]"}

data: {"event": "citation", "marker": 1, "source": "...", "title": "...", "cited_text": "..."}

data: {"event": "done", "session_id": "abc123", "request_id": "...", "model": "claude-haiku-4-5", "citations": [...]}
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
| `stream` | boolean | No | Enable SSE streaming (default: false) |
| `model` | string | No | `claude-haiku-4-5` or `claude-sonnet-5`; any other id requires an OpenRouter key |
| `page_context` | object | No | Page the widget is embedded in, so the assistant can answer about it |

### Chat Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User message |
| `session_id` | string | No | Session ID for multi-turn chat |
| `stream` | boolean | No | Enable SSE streaming (default: true) |
| `model` | string | No | `claude-haiku-4-5` or `claude-sonnet-5`; any other id requires an OpenRouter key |
| `page_context` | object | No | Page the widget is embedded in, so the assistant can answer about it |

## Response Fields

Both endpoints return these alongside the answer:

| Field | Type | Description |
|-------|------|-------------|
| `citations` | array | `marker`, `source`, `title`, `cited_text` per cited source, in marker order; empty when nothing was cited |
| `tool_calls` | array | Tools called while answering |
| `model` | string | The model that actually answered |
| `request_id` | string | Identifier to attach to feedback about this answer |

## Headers

| Header | Description | Required |
|--------|-------------|----------|
| `X-Anthropic-API-Key` | Claude Platform API key (BYOK); preferred when both BYOK headers are sent | No |
| `X-OpenRouter-Key` | OpenRouter API key (BYOK) | No |
| `X-API-Key` | Server admin API key | Only where the deployment requires auth and no BYOK header is sent |
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
    headers={"X-Anthropic-API-Key": "sk-ant-your-key"},
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
        headers={"X-Anthropic-API-Key": "sk-ant-your-key"},
    ) as response:
        for line in response.iter_lines():
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if data["event"] == "content":
                    print(data["content"], end="", flush=True)
                elif data["event"] == "citation":
                    print(f"\n[{data['marker']}] {data['title']}: {data['source']}")
```

## cURL Examples

### Ask (Non-streaming)

```bash
curl -X POST https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -H "X-Anthropic-API-Key: sk-ant-your-key" \
  -d '{"question": "What is HED?", "stream": false}'
```

### Ask (Streaming)

```bash
curl -N -X POST https://api.osc.earth/osa/hed/ask \
  -H "Content-Type: application/json" \
  -H "X-Anthropic-API-Key: sk-ant-your-key" \
  -d '{"question": "What is HED?", "stream": true}'
```

### Chat with Session

```bash
curl -X POST https://api.osc.earth/osa/hed/chat \
  -H "Content-Type: application/json" \
  -H "X-Anthropic-API-Key: sk-ant-your-key" \
  -d '{"message": "What is HED?", "stream": false}'

# Continue conversation with session_id from response
curl -X POST https://api.osc.earth/osa/hed/chat \
  -H "Content-Type: application/json" \
  -H "X-Anthropic-API-Key: sk-ant-your-key" \
  -d '{"message": "Tell me more", "session_id": "abc123", "stream": false}'
```
