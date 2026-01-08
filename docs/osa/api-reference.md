# API Reference

The OSA REST API provides programmatic access to the assistant.

## Base URL

```
http://localhost:38528
```

## Authentication

OSA supports two authentication modes:

### Server API Key

```bash
curl -H "X-API-Key: your-server-key" http://localhost:38528/chat
```

### BYOK (Bring Your Own Key)

Pass your OpenRouter API key directly:

```bash
curl -H "X-OpenRouter-Key: your-openrouter-key" http://localhost:38528/chat
```

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
  "version": "0.1.0"
}
```

### API Info

Get API information.

```
GET /info
```

Response:
```json
{
  "name": "Open Science Assistant",
  "version": "0.1.0",
  "assistants": ["hed", "bids", "eeglab"],
  "models": ["openai/gpt-4.1-mini", "anthropic/claude-3-5-haiku"]
}
```

### Chat

Send a message and receive a streaming response.

```
POST /chat
Content-Type: application/json

{
  "message": "How do I annotate a button press in HED?",
  "session_id": "optional-session-id",
  "assistant": "hed",
  "model": "openai/gpt-4.1-mini"
}
```

Response (Server-Sent Events):
```
data: {"type": "start", "session_id": "abc123"}

data: {"type": "token", "content": "To"}

data: {"type": "token", "content": " annotate"}

data: {"type": "tool_call", "tool": "retrieve_hed_docs", "params": {...}}

data: {"type": "tool_result", "tool": "retrieve_hed_docs", "result": {...}}

data: {"type": "token", "content": "..."}

data: {"type": "end", "usage": {"prompt_tokens": 1234, "completion_tokens": 567}}
```

## Request Parameters

### Chat Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User message |
| `session_id` | string | No | Session ID for multi-turn chat |
| `assistant` | string | No | Assistant to use (hed, bids, eeglab) |
| `model` | string | No | LLM model to use |

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid request",
  "detail": "Message is required"
}
```

### 401 Unauthorized

```json
{
  "error": "Unauthorized",
  "detail": "API key required"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal error",
  "detail": "LLM provider error"
}
```

## Python Client

```python
import httpx

async with httpx.AsyncClient() as client:
    async with client.stream(
        "POST",
        "http://localhost:38528/chat",
        json={"message": "What is HED?"},
        headers={"X-OpenRouter-Key": "your-key"},
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if data["type"] == "token":
                    print(data["content"], end="", flush=True)
```

## cURL Examples

### Basic Query

```bash
curl -X POST http://localhost:38528/chat \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"message": "What is HED?"}'
```

### With Session

```bash
curl -X POST http://localhost:38528/chat \
  -H "Content-Type: application/json" \
  -H "X-OpenRouter-Key: your-key" \
  -d '{"message": "Tell me more", "session_id": "my-session"}'
```
