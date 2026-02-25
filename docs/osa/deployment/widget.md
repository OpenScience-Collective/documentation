# Widget Deployment

The OSA Chat Widget is an embeddable JavaScript component that adds an AI assistant to any website. It connects to the OSA backend and provides a floating chat interface.

## Quick Integration

Add two script tags to your HTML:

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'hed'
  });
</script>
```

The widget appears as a chat bubble in the bottom-right corner of the page.

## How Configuration Works

Widget configuration uses a two-layer approach:

1. **YAML defaults** (community-level): Title, greeting, placeholder, suggested questions, theme color, and logo are defined in each community's `config.yaml` under the `widget` section. These are served by the `GET /communities` API endpoint.
2. **JavaScript overrides** (page-level): Embedders can override any field via `setConfig()`. Any value set in JavaScript takes precedence over the YAML defaults.

This means most embedders only need to set `communityId`; the widget fetches its display configuration from the API automatically.

## Configuration Options

### Display Options (from YAML defaults)

These fields are typically configured in the community's `config.yaml` and loaded automatically. You can override them per-page via `setConfig()`:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `communityId` | string | `'hed'` | Which community assistant to use |
| `title` | string | From YAML or community name | Widget header title |
| `initialMessage` | string | From YAML | First message shown to user |
| `placeholder` | string | From YAML or `'Ask a question...'` | Input placeholder text |
| `suggestedQuestions` | string[] | From YAML | Clickable suggestion buttons |
| `logo` | string | Auto-detected or from YAML | Logo URL for widget header avatar |
| `themeColor` | string | From YAML or `'#2563eb'` | Primary theme color (hex `#RRGGBB`) |

### Behavior Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
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
| `widgetInstructions` | string | `null` | Per-page context hint sent to the assistant (max 2000 chars) |

### Minimal Configuration

Only `communityId` is required. The widget fetches display settings (title, greeting, placeholder, suggested questions) from the `/communities` API automatically:

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'bids'
  });
</script>
```

### Per-Page Customization

Use `widgetInstructions` to give the assistant context about the specific page where the widget is embedded. This is sent to the backend as part of the page context and helps the assistant provide more relevant answers:

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'hed',
    widgetInstructions: 'The user is on the HED online validation tools page. Focus on helping with validation errors and tool usage.'
  });
</script>
```

This is useful when the same community assistant is embedded across multiple pages (e.g., documentation, tools, tutorials) and you want the assistant to adapt its responses to the page context.

### Full Configuration

```html
<script src="https://osa-demo.pages.dev/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'hed',
    title: 'HED Assistant',
    logo: 'https://example.com/hed-logo.png',
    themeColor: '#1a365d',
    initialMessage: 'Hi! I can help with HED annotations. What would you like to know?',
    placeholder: 'Ask about HED...',
    suggestedQuestions: [
      'What is HED?',
      'How do I annotate a button press?',
      'Validate my HED string',
      'What tools are available?'
    ],
    widgetInstructions: 'User is on the annotation guide page.',
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

The widget communicates with the following backend endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/communities` | GET | Fetch available communities and widget config |
| `/{communityId}/ask` | POST | Send a question, get a response |
| `/{communityId}/logo` | GET | Serve community logo image (if available) |
| `/health` | GET | Check backend status |

On load, the widget fetches `/communities` to get display configuration (title, greeting, placeholder, suggested questions, logo, theme color) for all available communities. This eliminates the need to hardcode these values in JavaScript.

### Request Format

```json
{
  "question": "What is HED?",
  "page_context": {
    "url": "https://hedtags.org/docs/getting-started",
    "title": "Getting Started - HED",
    "widget_instructions": "User is on the getting started page."
  }
}
```

The `widget_instructions` field is optional and only sent when configured via `setConfig({ widgetInstructions: '...' })`. The `cf_turnstile_response` field is also sent by the widget when Turnstile is configured, but this is consumed by the Cloudflare Worker proxy, not the backend API.

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

The demo page at [osa-demo.pages.dev](https://osa-demo.pages.dev) dynamically loads all available communities from the `/communities` API and showcases them with URL-based routing:

- `/` - Landing page with community cards (populated from API)
- `/{communityId}` - Community-specific assistant demo (e.g., `/hed`, `/bids`, `/eeglab`, `/fieldtrip`)

Each community page auto-configures the widget using the YAML-defined defaults. New communities added to the registry appear on the demo page automatically without frontend changes.

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
