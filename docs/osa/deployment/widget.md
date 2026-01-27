# Widget Deployment

The OSA Chat Widget is an embeddable JavaScript component that adds an AI assistant to any website. It connects to the OSA backend and provides a floating chat interface.

## Quick Integration

Add two script tags to your HTML:

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"
        crossorigin="anonymous"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'hed'
  });
</script>
```

The widget appears as a chat bubble in the bottom-right corner of the page.

!!! warning "Don't Use Integrity Hashes"
    Do **not** include `integrity="sha384-..."` hashes in the script tag. The widget is updated frequently with new features and bug fixes. Hardcoded integrity hashes will prevent the browser from loading updated versions, breaking the widget.

    The `crossorigin="anonymous"` attribute is sufficient for CORS protection. We control the deployment at `osa-demo.pages.dev`.

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `communityId` | string | `'hed'` | Which community assistant to use |
| `title` | string | `'HED Assistant'` | Widget header title |
| `initialMessage` | string | HED greeting | First message shown to user |
| `placeholder` | string | `'Ask about HED...'` | Input placeholder text |
| `suggestedQuestions` | string[] | HED questions | Clickable suggestion buttons |
| `apiEndpoint` | string | Auto-detected | Backend API URL |
| `storageKey` | string | Auto-derived | localStorage key for chat history |
| `turnstileSiteKey` | string | `null` | Cloudflare Turnstile site key |
| `showExperimentalBadge` | boolean | `true` | Show beta/experimental badge |
| `repoUrl` | string | OSA GitHub URL | URL for the "Powered by" footer link |
| `repoName` | string | `'Open Science Assistant'` | Display name in footer |
| `allowPageContext` | boolean | `true` | Show page context toggle |
| `pageContextDefaultEnabled` | boolean | `true` | Default state of page context |
| `pageContextStorageKey` | string | `'osa-page-context-enabled'` | localStorage key for page context preference |
| `pageContextLabel` | string | `'Share page URL...'` | Label text for the page context checkbox |
| `fullscreen` | boolean | `false` | Open chat in fullscreen mode |
| `streamingEnabled` | boolean | `true` | Enable progressive text display via Server-Sent Events |

### Minimal Configuration

Only `communityId` is required. Everything else has sensible defaults:

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'bids'
  });
</script>
```

### Full Configuration

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'hed',
    title: 'HED Assistant',
    initialMessage: 'Hi! I can help with HED annotations. What would you like to know?',
    placeholder: 'Ask about HED...',
    suggestedQuestions: [
      'What is HED?',
      'How do I annotate a button press?',
      'Validate my HED string',
      'What tools are available?'
    ],
    showExperimentalBadge: false,
    allowPageContext: true,
    pageContextDefaultEnabled: true
  });
</script>
```

## Features

### Page Context Awareness

When enabled, the widget can share the current page's URL and title with the assistant. This helps provide contextually relevant answers when the widget is embedded on documentation pages.

Users can toggle this via a checkbox in the widget. The preference is persisted in localStorage.

### Chat History

Conversations are persisted in localStorage using a key derived from the `communityId`. Each community has its own chat history. Users can clear history via the reset button.

### Health Status

The widget shows backend connectivity status (Online/Offline) via a status indicator. It checks the `/health` endpoint on load.

### Resizable Window

Users can resize the chat window by dragging the top-left corner. The size is not persisted across page loads.

### Pop-out Window

Users can open the chat in a separate browser window for a larger workspace. The pop-out window shares the same session.

### Markdown Rendering

Assistant responses support full Markdown rendering including:

- Tables
- Code blocks with copy button
- Lists (ordered and unordered)
- Links
- Bold and italic

### Streaming Responses

The widget supports Server-Sent Events (SSE) streaming for progressive text display. When enabled (default), assistant responses appear word-by-word as they're generated, providing better user experience especially with slower models.

**Features:**
- Real-time text streaming with 100ms UI updates
- Tool execution logging (visible in console)
- Graceful error recovery with partial content preservation
- 60-second stream timeout protection
- Automatic fallback to non-streaming if backend doesn't support SSE

**Configuration:**

```javascript
OSAChatWidget.setConfig({
  communityId: 'hed',
  streamingEnabled: true  // Enable streaming (default)
});
```

Streaming is enabled by default. To disable:

```javascript
OSAChatWidget.setConfig({
  communityId: 'hed',
  streamingEnabled: false  // Wait for complete response
});
```

**Technical Details:**

The widget detects streaming responses by checking for `Content-Type: text/event-stream`. When detected, it parses SSE events and updates the UI progressively. Events include:

- `content`: Text chunks to display
- `tool_start` / `tool_end`: Tool execution lifecycle
- `done`: Streaming complete
- `error`: Backend error with message

## Environment Detection

The widget auto-detects the environment based on the hostname:

| Hostname Pattern | Backend |
|-----------------|---------|
| `develop.*` | Dev worker (`osa-worker-dev`) |
| `localhost` / `127.0.0.1` | Dev worker |
| Everything else | Production worker (`osa-worker`) |

Override with `apiEndpoint`:

```javascript
OSAChatWidget.setConfig({
  communityId: 'hed',
  apiEndpoint: 'https://your-custom-backend.example.com'
});
```

## Bot Protection

The widget supports Cloudflare Turnstile for bot protection:

```javascript
OSAChatWidget.setConfig({
  communityId: 'hed',
  turnstileSiteKey: '0x4AAAAAA...'
});
```

When configured, users must complete a Turnstile challenge before sending messages. The token is included in API requests.

## API Endpoints

The widget communicates with two backend endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{communityId}/ask` | POST | Send a question, get a response |
| `/health` | GET | Check backend status |

### Request Format

```json
{
  "question": "What is HED?",
  "page_context": {
    "url": "https://hedtags.org/docs/getting-started",
    "title": "Getting Started - HED"
  }
}
```

The `cf_turnstile_response` field is also sent by the widget when Turnstile is configured, but this is consumed by the Cloudflare Worker proxy, not the backend API.

### Response Format

```json
{
  "answer": "HED (Hierarchical Event Descriptors) is...",
  "tool_calls": []
}
```

## Self-Hosting

To host the widget yourself:

1. Copy `osa-chat-widget.js` from the [frontend directory](https://github.com/OpenScience-Collective/osa/tree/main/frontend)
2. Serve it from your static file server
3. Update the script `src` to point to your hosted copy
4. Set `apiEndpoint` to your OSA backend

```html
<script src="https://your-cdn.example.com/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'my-tool',
    apiEndpoint: 'https://your-backend.example.com'
  });
</script>
```

## Demo Page

The demo page at [osa-demo.pages.dev](https://osa-demo.pages.dev) showcases all available community assistants with URL-based routing:

- `/` - Landing page with community cards
- `/hed` - HED assistant demo
- `/bids` - BIDS assistant demo
- `/eeglab` - EEGLAB assistant demo

Each community page auto-configures the widget with the appropriate settings.

## Troubleshooting

**Widget doesn't appear:**

- Check browser console for JavaScript errors
- Verify the script URL is accessible
- Ensure `communityId` contains only letters, numbers, hyphens, and underscores (the backend registry uses kebab-case IDs)

**"Offline" status:**

- The backend may be down or unreachable
- Check if `apiEndpoint` is correct for your environment
- Network policies (CORS, CSP) may be blocking requests

**Chat history not persisting:**

- localStorage may be disabled or full
- Private/incognito browsing clears localStorage on close
- Different `communityId` values use different storage keys

**Page context not working:**

- Ensure `allowPageContext: true` (default)
- User must enable the checkbox in the widget
- The page URL is sent; the backend fetches the content
