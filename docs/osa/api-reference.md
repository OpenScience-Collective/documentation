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
