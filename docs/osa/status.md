# Sync Status

<div id="status-container">
  <div class="status-loading">Loading status...</div>
</div>

<style>
.status-loading {
  padding: 2rem;
  text-align: center;
  color: var(--md-default-fg-color--light);
}

.status-error {
  padding: 1rem;
  background: var(--md-code-bg-color);
  border-left: 4px solid #f44336;
  margin: 1rem 0;
}

.status-grid {
  display: grid;
  gap: 1.5rem;
  margin-top: 1rem;
}

.status-card {
  background: var(--md-code-bg-color);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--md-default-fg-color--lightest);
}

.status-card h3 {
  margin-top: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.status-healthy { background: #4caf50; }
.status-warning { background: #ff9800; }
.status-error-indicator { background: #f44336; }

.status-details {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem 1rem;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.status-label {
  color: var(--md-default-fg-color--light);
}

.status-value {
  font-family: var(--md-code-font-family);
}

.scheduler-info {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--md-default-fg-color--lightest);
}

.repo-list, .source-list {
  margin-top: 0.5rem;
  padding-left: 1rem;
  font-size: 0.85rem;
}

.repo-item, .source-item {
  padding: 0.25rem 0;
  color: var(--md-default-fg-color--light);
}

.last-updated {
  margin-top: 1.5rem;
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
  text-align: center;
}

.refresh-btn {
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-top: 1rem;
}

.refresh-btn:hover {
  opacity: 0.9;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

<script>
// API endpoint - allow override via query param for development/testing
// Usage: ?api=http://localhost:38528 for local testing
const urlParams = new URLSearchParams(window.location.search);
const API_BASE = urlParams.get('api') || 'https://api.osc.earth/osa';

// HTML escape to prevent XSS from API response data
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

async function fetchStatus() {
  const container = document.getElementById('status-container');

  try {
    const response = await fetch(`${API_BASE}/sync/status`);

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();
    renderStatus(container, data);
  } catch (error) {
    renderError(container, error);
  }
}

function formatDate(isoString) {
  if (!isoString) return 'Never';
  try {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZoneName: 'short'
    });
  } catch {
    return 'Invalid date';
  }
}

function formatAge(hours) {
  if (hours === null || hours === undefined) return 'Never synced';
  if (hours < 1) return 'Less than an hour ago';
  if (hours < 24) return `${Math.round(hours)} hours ago`;
  const days = Math.round(hours / 24);
  return `${days} day${days === 1 ? '' : 's'} ago`;
}

function getHealthClass(healthy) {
  return healthy ? 'status-healthy' : 'status-error-indicator';
}

function getHealthText(healthy, ageHours) {
  if (healthy) return 'Healthy';
  if (ageHours === null) return 'Pending';
  return 'Stale';
}

function renderStatus(container, data) {
  const github = data?.github || {};
  const papers = data?.papers || {};
  const scheduler = data?.scheduler || {};
  const health = data?.health || {};

  container.innerHTML = `
    <div class="status-grid">
      <div class="status-card">
        <h3>
          <span class="status-indicator ${getHealthClass(health.github_healthy)}"></span>
          GitHub Sync
        </h3>
        <div class="status-details">
          <span class="status-label">Status:</span>
          <span class="status-value">${escapeHtml(getHealthText(health.github_healthy, health.github_age_hours))}</span>

          <span class="status-label">Last sync:</span>
          <span class="status-value">${escapeHtml(formatAge(health.github_age_hours))}</span>

          <span class="status-label">Total items:</span>
          <span class="status-value">${(github.total_items ?? 0).toLocaleString()}</span>

          <span class="status-label">Issues:</span>
          <span class="status-value">${(github.issues ?? 0).toLocaleString()}</span>

          <span class="status-label">Pull Requests:</span>
          <span class="status-value">${(github.prs ?? 0).toLocaleString()}</span>

          <span class="status-label">Open items:</span>
          <span class="status-value">${(github.open_items ?? 0).toLocaleString()}</span>
        </div>

        <div class="repo-list">
          <strong>Repositories:</strong>
          ${Object.entries(github.repos || {}).map(([repo, info]) => `
            <div class="repo-item">
              ${escapeHtml(repo)}: ${(info?.items ?? 0)} items
              ${info?.last_sync ? `(synced ${escapeHtml(formatDate(info.last_sync))})` : ''}
            </div>
          `).join('')}
        </div>
      </div>

      <div class="status-card">
        <h3>
          <span class="status-indicator ${getHealthClass(health.papers_healthy)}"></span>
          Papers Sync
        </h3>
        <div class="status-details">
          <span class="status-label">Status:</span>
          <span class="status-value">${escapeHtml(getHealthText(health.papers_healthy, health.papers_age_hours))}</span>

          <span class="status-label">Last sync:</span>
          <span class="status-value">${escapeHtml(formatAge(health.papers_age_hours))}</span>

          <span class="status-label">Total papers:</span>
          <span class="status-value">${(papers.total_items ?? 0).toLocaleString()}</span>
        </div>

        <div class="source-list">
          <strong>Sources:</strong>
          ${Object.entries(papers.sources || {}).map(([source, info]) => `
            <div class="source-item">
              ${escapeHtml(source)}: ${(info?.items ?? 0)} papers
              ${info?.last_sync ? `(synced ${escapeHtml(formatDate(info.last_sync))})` : ''}
            </div>
          `).join('')}
        </div>
      </div>

      <div class="status-card scheduler-info">
        <h3>Scheduler</h3>
        <div class="status-details">
          <span class="status-label">Enabled:</span>
          <span class="status-value">${scheduler.enabled ? 'Yes' : 'No'}</span>

          <span class="status-label">Running:</span>
          <span class="status-value">${scheduler.running ? 'Yes' : 'No'}</span>

          <span class="status-label">GitHub schedule:</span>
          <span class="status-value">${escapeHtml(scheduler.github_cron ?? 'Not configured')} (UTC)</span>

          <span class="status-label">Papers schedule:</span>
          <span class="status-value">${escapeHtml(scheduler.papers_cron ?? 'Not configured')} (UTC)</span>

          ${scheduler.next_github_sync ? `
            <span class="status-label">Next GitHub sync:</span>
            <span class="status-value">${escapeHtml(formatDate(scheduler.next_github_sync))}</span>
          ` : ''}

          ${scheduler.next_papers_sync ? `
            <span class="status-label">Next papers sync:</span>
            <span class="status-value">${escapeHtml(formatDate(scheduler.next_papers_sync))}</span>
          ` : ''}
        </div>
      </div>
    </div>

    <div class="last-updated">
      Last checked: ${escapeHtml(new Date().toLocaleString())}
      <br>
      <button class="refresh-btn" onclick="refreshStatus()">Refresh</button>
    </div>
  `;
}

function renderError(container, error) {
  // Detect likely CORS or network issues
  let hint = 'The API may be temporarily unavailable. Try again later.';
  if (error instanceof TypeError && error.message.includes('fetch')) {
    hint = 'Unable to reach the API. This may be a network or CORS issue.';
  }

  container.innerHTML = `
    <div class="status-error">
      <strong>Unable to fetch status</strong>
      <p>${escapeHtml(error.message)}</p>
      <p>${escapeHtml(hint)}</p>
      <button class="refresh-btn" onclick="refreshStatus()">Retry</button>
    </div>
  `;
}

async function refreshStatus() {
  const btn = document.querySelector('.refresh-btn');
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Refreshing...';
  }

  await fetchStatus();

  if (btn) {
    btn.disabled = false;
    btn.textContent = 'Refresh';
  }
}

// Fetch status on page load
document.addEventListener('DOMContentLoaded', fetchStatus);
</script>

## About This Page

This page shows the real-time status of OSA's knowledge sync jobs. The knowledge database automatically syncs:

- **GitHub Issues/PRs**: Daily at 2am UTC from HED repositories
- **Academic Papers**: Weekly Sunday at 3am UTC from OpenALEX, Semantic Scholar, and PubMed

### Health Indicators

| Status | Meaning |
|--------|---------|
| :material-circle:{ style="color: #4caf50" } Healthy | Sync completed within expected timeframe |
| :material-circle:{ style="color: #ff9800" } Pending | Never synced (new installation) |
| :material-circle:{ style="color: #f44336" } Stale | Sync is overdue |

### API Endpoint

The status data is fetched from the OSA API:

```
GET /sync/status
```

Returns JSON with `github`, `papers`, `scheduler`, and `health` objects.

!!! tip "Local Testing"
    To test with a local API server, add `?api=http://localhost:38528` to this page's URL.
