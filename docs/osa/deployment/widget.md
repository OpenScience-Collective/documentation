# Widget Deployment

The OSA Chat Widget is an embeddable JavaScript component that adds an AI assistant to any website. It connects to the OSA backend and provides a floating chat interface.

## Quick Integration

Add two script tags to your HTML:

```html
<script src="https://demo.osc.earth/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'hed'
  });
</script>
```

The `<script>` tag that loads the widget must come first, so that
`window.OSAChatWidget` exists before the inline `setConfig()` call runs.
Do not add `defer` or `async` to that tag unless you also add
`data-no-auto-init` and call `OSAChatWidget.init()` yourself; see
[Loading the Script Asynchronously](#loading-the-script-asynchronously).

The widget appears as a chat bubble in the bottom-right corner of the page.

!!! note "Existing embeds on osa-demo.pages.dev"
    Sites that already load the widget from `https://osa-demo.pages.dev/osa-chat-widget.js`
    keep working; that address is not going away.
    New embeds should use `https://demo.osc.earth/osa-chat-widget.js` instead.

## Loading the Script Asynchronously

The widget defines `window.OSAChatWidget` when its script runs, and it
auto-initializes as soon as the page is ready. If you need to load the
script with `defer` or `async` (for example, to keep it out of the
critical rendering path), add `data-no-auto-init` to the script tag and
call `setConfig()` and `init()` from an `onload` handler instead:

```html
<script
  src="https://demo.osc.earth/osa-chat-widget.js"
  defer
  data-no-auto-init
  onload="OSAChatWidget.setConfig({ communityId: 'hed' }); OSAChatWidget.init();">
</script>
```

Do not add `defer` or `async` to the script tag while still relying on a
separate inline `setConfig()` call: the deferred script has not run yet
when the inline block executes, `window.OSAChatWidget` does not exist,
and the call throws `ReferenceError: OSAChatWidget is not defined`.

## Pinning to a Release with Subresource Integrity

Security-sensitive environments that require Subresource Integrity (SRI)
can pin the widget to a specific release using a versioned jsDelivr URL.
The `integrity` hash for each release is published on the
[GitHub releases page](https://github.com/OpenScience-Collective/osa/releases).

```html
<!-- Replace vX.Y.Z and the integrity hash from the GitHub release notes -->
<script
  src="https://cdn.jsdelivr.net/gh/OpenScience-Collective/osa@vX.Y.Z/frontend/osa-chat-widget.js"
  integrity="sha384-..."
  crossorigin="anonymous">
</script>
<script>
  OSAChatWidget.setConfig({ communityId: 'hed' });
</script>
```

Do not add `defer` to the pinned `<script>` tag unless you also add
`data-no-auto-init` and initialize the widget from an `onload` handler,
per [Loading the Script Asynchronously](#loading-the-script-asynchronously)
above; otherwise the inline `setConfig()` call runs before the script
has defined `OSAChatWidget`.

You must update the version tag by hand when upgrading; SRI pinning does
not follow new releases automatically.

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
| `repoUrl` | string | `'https://osc.earth/osa/'` | URL for the "Powered by" footer link |
| `repoName` | string | `'Open Science Assistant'` | Display name in footer |
| `allowPageContext` | boolean | `true` | Show page context toggle |
| `pageContextDefaultEnabled` | boolean | `true` | Default state of page context |
| `pageContextStorageKey` | string | `'osa-page-context-enabled'` | localStorage key for page context preference |
| `pageContextLabel` | string | `'Share page URL...'` | Label text for the page context checkbox |
| `fullscreen` | boolean | `false` | Open chat in fullscreen mode |
| `disclaimerEnabled` | boolean | `true` | Show AI disclaimer above footer |
| `disclaimerText` | string | `'This is an AI assistant and may make mistakes.'` | Disclaimer message text |
| `disclaimerColor` | string | `'#9a3412'` | Disclaimer text color |
| `disclaimerBackground` | string | `'#fff7ed'` | Disclaimer background color |
| `widgetInstructions` | string | `null` | Per-page context hint sent to the assistant (max 2000 chars) |

### Minimal Configuration

Only `communityId` is required. The widget fetches display settings (title, greeting, placeholder, suggested questions) from the `/communities` API automatically:

```html
<script src="https://demo.osc.earth/osa-chat-widget.js"></script>
<script>
  OSAChatWidget.setConfig({
    communityId: 'bids'
  });
</script>
```

### Per-Page Customization

Use `widgetInstructions` to give the assistant context about the specific page where the widget is embedded. This is sent to the backend as part of the page context and helps the assistant provide more relevant answers:

```html
<script src="https://demo.osc.earth/osa-chat-widget.js"></script>
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
<script src="https://demo.osc.earth/osa-chat-widget.js"></script>
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
    pageContextDefaultEnabled: true,
    disclaimerText: 'AI-powered assistant. Responses may contain errors.',
    disclaimerColor: '#92400e',
    disclaimerBackground: '#fffbeb'
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

The widget auto-detects its backend from the hostname of the page it is
embedded on (`window.location.hostname`), not from where the widget script
itself was loaded:

| Embedding page's hostname | Backend |
|---|---|
| `demo.osc.earth` or `osa-demo.pages.dev` | Production: `https://widget.osc.earth/osa` |
| Ends with `-demo.osc.earth` or `.osa-demo.pages.dev`, or contains `localhost` or `127.0.0.1` | Develop: `https://develop-widget.osc.earth/osa` |
| Anything else (an adopter's own domain) | Production: `https://widget.osc.earth/osa` |

This means an adopter testing the widget on `localhost` talks to the develop
backend by default. Set `apiEndpoint` explicitly to point at production
instead:

```javascript
OSAChatWidget.setConfig({
  communityId: 'hed',
  apiEndpoint: 'https://widget.osc.earth/osa'
});
```

`apiEndpoint` also accepts any other reachable OSA backend, such as a
self-hosted deployment.

## Cross-Origin Requests (CORS)

Without a bring-your-own key (see [Authentication](../api-reference.md#authentication)),
the backend only answers a widget request whose `Origin` header is
authorized for that community. Two platform origins,
`https://demo.osc.earth` and `https://osa-demo.pages.dev`, are always
authorized for every community. Any other origin, such as an adopter's
own domain, must be added to that community's `cors_origins` in its
`config.yaml`:

```yaml
cors_origins:
  - https://mysite.com
  - https://www.mysite.com
```

Without either a listed origin or a BYOK header, the backend responds
with 403 and "API key required." Adding an origin requires a pull
request to the community's `config.yaml`, so a new deployment should
open one before going live on a new domain.

## Content Security Policy (CSP)

A page with a Content Security Policy needs to allow the widget's script
host, its API host, and the community logo's host. For the default
`demo.osc.earth`-hosted script talking to the production backend:

```
script-src 'self' https://demo.osc.earth;
connect-src 'self' https://widget.osc.earth;
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
```

- `script-src` needs the host the widget script itself loads from:
  `https://demo.osc.earth` for the quick-start snippet, or
  `https://cdn.jsdelivr.net` when pinned to a release with SRI.
- `connect-src` needs the widget's backend: `https://widget.osc.earth`
  in production, or `https://develop-widget.osc.earth` in development
  (see [Environment Detection](#environment-detection)).
- `style-src` needs `'unsafe-inline'`: the widget injects its own
  stylesheet at runtime rather than loading an external one.
- `img-src` needs whichever host serves the community's logo, plus
  `data:` if a logo is ever inlined.

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

The demo page at [demo.osc.earth](https://demo.osc.earth) (also served from the
`osa-demo.pages.dev` address that existing embeds use) dynamically loads all available
communities from the `/communities` API and showcases them with URL-based routing:

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
