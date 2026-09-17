# Troubleshooting Guide

Common issues and solutions for OSA community onboarding and operations.

---

## Quick Diagnostic Checklist

Before diving into specific errors:

1. **Validate your config:**
   ```bash
   uv run osa validate src/assistants/your-community/config.yaml
   ```

2. **Check environment variables:**

    === "macOS"

        ```bash
        echo $ANTHROPIC_API_KEY_YOUR_COMMUNITY
        # Should print your API key, not empty
        ```

    === "Linux"

        ```bash
        echo $ANTHROPIC_API_KEY_YOUR_COMMUNITY
        # Should print your API key, not empty
        ```

    === "Windows"

        ```powershell
        echo $env:ANTHROPIC_API_KEY_YOUR_COMMUNITY
        # Should print your API key, not empty
        ```

    If your community funds itself through OpenRouter instead, the variable is
    named `OPENROUTER_API_KEY_YOUR_COMMUNITY`; everything below works the same
    way, against OpenRouter rather than Anthropic.

3. **Test API key:**
   ```bash
   uv run osa validate src/assistants/your-community/config.yaml --test-api-key
   ```

4. **Check server status:**
   ```bash
   uv run osa health
   ```

---

## Configuration Validation Errors

### Error: YAML Syntax Error

**Symptom:**
```
YAML syntax error at line 15, column 3: mapping values are not allowed here
```

**Causes:**
- Incorrect indentation (must use spaces, not tabs)
- Missing colon after key
- Improper list formatting
- Special characters not quoted

**Solutions:**

**Check indentation:**
```yaml
# Wrong - using tabs
documentation:
	- title: My Doc

# Correct - using spaces
documentation:
  - title: My Doc
```

**Quote special characters:**
```yaml
# Wrong - colon in unquoted string
description: HED: Event annotation

# Correct - quoted
description: "HED: Event annotation"
```

**List formatting:**
```yaml
# Wrong - missing dash
cors_origins:
  https://example.com

# Correct - with dash
cors_origins:
  - https://example.com
```

**Validation:**
```bash
# Use a YAML validator
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

---

### Error: Community ID must be kebab-case

**Symptom:**
```
Community ID must be kebab-case (lowercase, hyphens): MyProject
```

**Cause:**
Community ID contains uppercase letters, underscores, or invalid characters.

**Solution:**
```yaml
# Wrong
id: MyProject
id: my_project
id: my.project
id: -myproject   # Leading hyphen

# Correct
id: myproject
id: my-project
id: my-project-2024
```

**Rules:**
- Lowercase letters only
- Numbers allowed
- Hyphens allowed (not leading/trailing)
- No underscores, dots, or spaces

---

### Error: Invalid CORS origin

**Symptom:**
```
Invalid CORS origin 'example.com'. Must be a valid origin (e.g., 'https://example.org')
```

**Cause:**
CORS origin missing scheme or improperly formatted.

**Solution:**
```yaml
# Wrong - missing scheme
cors_origins:
  - example.com
  - www.example.com

# Wrong - includes path
cors_origins:
  - https://example.com/docs

# Correct
cors_origins:
  - https://example.com
  - https://www.example.com
  - https://*.pages.dev
```

**Common Mistakes:**
- Forgetting `https://` prefix
- Including path (`/docs`)
- Including query string (`?foo=bar`)
- Using `*` alone (not allowed)

---

### Error: Preload requires source_url

**Symptom:**
```
DocSource 'My Doc' has preload=True but no source_url
```

**Cause:**
Document configured with `preload: true` but missing `source_url` field.

**Solution:**
```yaml
# Wrong - preload without source_url
documentation:
  - title: Core Docs
    url: https://example.com/docs
    preload: true

# Correct - source_url provided
documentation:
  - title: Core Docs
    url: https://example.com/docs
    source_url: https://raw.githubusercontent.com/org/repo/main/docs.md
    preload: true
```

**Why:**
Preloaded documents are fetched and embedded in the system prompt. The `source_url` must point to the raw markdown or text content.

---

### Error: Repository must be in 'org/repo' format

**Symptom:**
```
Repository must be in 'org/repo' format, got: hed-specification
```

**Cause:**
GitHub repository missing organization prefix.

**Solution:**
```yaml
# Wrong - missing org
github:
  repos:
    - hed-specification

# Correct - org/repo format
github:
  repos:
    - hed-standard/hed-specification
```

---

### Error: Invalid DOI format

**Symptom:**
```
Invalid DOI format (expected '10.xxxx/yyyy'): doi.org/10.1234/example
```

**Cause:**
DOI includes URL prefix or doesn't match expected format.

**Solution:**
```yaml
# Wrong - includes prefix
citations:
  dois:
    - https://doi.org/10.1234/example
    - doi.org/10.1234/example

# Correct - DOI only
citations:
  dois:
    - 10.1234/example
```

**Valid DOI Format:**
- Must start with `10.`
- Format: `10.xxxx/yyyy`
- No URL prefixes

---

## API Key Issues

### Warning: API key env var not set

**Symptom:**
```
ANTHROPIC_API_KEY_MYPROJECT not set
Validation passed with warnings
```

**Impact:**
- Assistant will fall back to platform API key
- Costs billed to platform, not your community
- Shared rate limits apply

**Solution:**

**For local testing:**

=== "macOS"

    ```bash
    # Add to shell profile
    echo 'export ANTHROPIC_API_KEY_MYPROJECT="sk-ant-..."' >> ~/.zshrc
    source ~/.zshrc

    # Verify
    echo $ANTHROPIC_API_KEY_MYPROJECT
    ```

=== "Linux"

    ```bash
    # Add to shell profile
    echo 'export ANTHROPIC_API_KEY_MYPROJECT="sk-ant-..."' >> ~/.bashrc
    source ~/.bashrc

    # Verify
    echo $ANTHROPIC_API_KEY_MYPROJECT
    ```

=== "Windows"

    ```powershell
    # Set for current session
    $env:ANTHROPIC_API_KEY_MYPROJECT = "sk-ant-..."

    # Set permanently (persists across sessions)
    [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY_MYPROJECT", "sk-ant-...", "User")

    # Verify
    echo $env:ANTHROPIC_API_KEY_MYPROJECT
    ```

**For production (server):**
```bash
# Add to .env file
echo 'ANTHROPIC_API_KEY_MYPROJECT="sk-ant-..."' >> .env
```

**Verify:**
```bash
uv run osa validate src/assistants/myproject/config.yaml
# Should show: "✓ ANTHROPIC_API_KEY_MYPROJECT is set (Anthropic)"
```

The env var name must match `ANTHROPIC_API_KEY_[A-Z0-9_]+`, so that a config
cannot point the assistant at an unrelated secret.
A community whose config sets `openrouter_api_key_env_var` instead is reported
the same way, as `(OpenRouter)`, and its variable must match
`OPENROUTER_API_KEY_[A-Z0-9_]+`.
If a config sets both, the Anthropic key is the one that pays, and the one
`osa validate` reports.

---

### Error: API key test failed (401 Unauthorized)

**Symptom:**
```
Invalid API key (401 Unauthorized)
```

**Causes:**
- API key is invalid or expired
- Wrong key format
- Key revoked in the Anthropic Console

**Solution:**

1. **Verify key format:**

    === "macOS"

        ```bash
        echo $ANTHROPIC_API_KEY_MYPROJECT
        # Should start with: sk-ant-
        ```

    === "Linux"

        ```bash
        echo $ANTHROPIC_API_KEY_MYPROJECT
        # Should start with: sk-ant-
        ```

    === "Windows"

        ```powershell
        echo $env:ANTHROPIC_API_KEY_MYPROJECT
        # Should start with: sk-ant-
        ```

2. **Check the key in the Anthropic Console:**
   - Visit https://platform.claude.com/settings/keys
   - Verify key exists and is active
   - Check that the workspace it belongs to has not hit a spend limit

3. **Generate new key if needed:**
   - Go to https://platform.claude.com/settings/keys
   - Create new API key
   - Update environment variable

4. **Test directly:**
   ```bash
   curl https://api.anthropic.com/v1/models \
     -H "x-api-key: $ANTHROPIC_API_KEY_MYPROJECT" \
     -H "anthropic-version: 2023-06-01"
   # Should return 200 OK with model list
   ```

    A community key is used against Anthropic's own API rather than the
    platform's endpoint on AWS, because it is not authorized on the platform's
    workspace.
    That is the endpoint `--test-api-key` probes too, so the curl above and the
    validator agree.

    For an OpenRouter community key, the equivalent is:

    ```bash
    curl https://openrouter.ai/api/v1/models \
      -H "Authorization: Bearer $OPENROUTER_API_KEY_MYPROJECT"
    ```

---

### Error: API key test failed (403 Forbidden)

**Symptom:**
```
API key lacks permissions (403 Forbidden)
```

**Cause:**
API key doesn't have necessary permissions, or the account has no funds left.

**Solution:**

1. **Check the account balance:**
   - Visit https://platform.claude.com/settings/billing
   - Ensure the account has credit available
   - For an OpenRouter community key, check https://openrouter.ai/credits instead

2. **Check key permissions:**
   - A key scoped to one workspace cannot spend from another
   - Verify the key has access to the models you want to use

3. **Add funds:**
   - Top up the account, or raise the workspace spend limit
   - Test again afterwards

---

## Runtime Errors

### Error: CORS policy blocked

**Browser Console:**
```
Access to fetch at 'https://api.osc.earth/osa/...' from origin 'https://mysite.com'
has been blocked by CORS policy
```

**Cause:**
Your website origin not listed in `cors_origins` config.

**Solution:**

1. **Add your origin to config:**
   ```yaml
   cors_origins:
     - https://mysite.com
     - https://www.mysite.com  # Don't forget www variant
   ```

2. **Redeploy assistant** (config changes require restart)

3. **Verify origin exactly matches:**
   ```javascript
   // In browser console
   console.log(window.location.origin)
   // Must match exactly (including https://)
   ```

**Common Issues:**
- Forgot `www` subdomain variant
- `http://` vs `https://` mismatch
- Port number missing (e.g., `:3000`)
- Trailing slash in config (remove it)

---

### Error: Widget not loading

**Symptom:**
Widget icon doesn't appear or widget doesn't open.

**Causes:**
1. Script not loaded
2. Wrong community ID
3. API endpoint unreachable
4. JavaScript errors

**Diagnosis:**

1. **Check browser console** (F12 -> Console):
   ```
   Look for errors like:
   - Failed to load widget.js
   - OSAWidget is not defined
   - Community 'xxx' not found
   ```

2. **Verify script loads:**
   ```html
   <!-- Check this in your HTML -->
   <script src="https://api.osc.earth/osa/widget.js"></script>
   ```

3. **Check network tab:**
   - Widget.js should load (200 OK)
   - API requests should succeed

**Solutions:**

**Wrong community ID:**
```html
<!-- Wrong - ID doesn't match config -->
<script>
    OSAWidget.init({
        communityId: 'wrong-id'  // Check this matches config.yaml
    });
</script>

<!-- Correct -->
<script>
    OSAWidget.init({
        communityId: 'hed'  // Must match config.yaml id field
    });
</script>
```

**Script placement:**
```html
<!-- Wrong - script in <head> before widget init -->
<head>
    <script>
        OSAWidget.init({ communityId: 'hed' });
    </script>
    <script src="https://api.osc.earth/osa/widget.js"></script>
</head>

<!-- Correct - load script first -->
<body>
    <script src="https://api.osc.earth/osa/widget.js"></script>
    <script>
        OSAWidget.init({ communityId: 'hed' });
    </script>
</body>
```

**API endpoint:**
```javascript
// Check if API is reachable
fetch('https://api.osc.earth/osa/health')
    .then(r => r.json())
    .then(console.log);
// Should show: {status: "healthy"}
```

---

### Error: Messages not getting responses

**Symptom:**
Widget accepts input but shows loading spinner indefinitely.

**Causes:**
1. API key not configured
2. Network errors
3. Model timeout
4. Backend server down

**Diagnosis:**

1. **Check browser network tab:**
   - Look for failed API requests
   - Check response status codes
   - Look for timeout errors

2. **Check API health:**
   ```bash
   curl https://api.osc.earth/osa/health
   ```

3. **Check backend logs** (if you have access):
   ```bash
   docker logs osa-prod
   ```

**Solutions:**

**API key missing:**
- Verify `anthropic_api_key_env_var` is set on server, or `openrouter_api_key_env_var` for a community funded through OpenRouter
- Check env var exists: `echo $ANTHROPIC_API_KEY_XXX`
- Restart server after adding env var

**Network errors:**
- Check firewall rules
- Verify API endpoint accessible
- Check DNS resolution

**Timeouts:**
- May indicate model is slow or overloaded
- Try `claude-haiku-4-5`, which is the faster of the two offered models
- Check [status.anthropic.com](https://status.anthropic.com), or OpenRouter's status page for an OpenRouter community

---

## Deployment Issues

### Error: Config file not found

**Symptom:**
```
Error: Config file not found: src/assistants/myproject/config.yaml
```

**Cause:**
Config file not in expected location or path incorrect.

**Solution:**

1. **Check file exists:**
   ```bash
   ls src/assistants/myproject/config.yaml
   ```

2. **Verify directory structure:**
   ```
   src/assistants/
   └── myproject/
       └── config.yaml
   ```

3. **Check file name:**
   - Must be exactly `config.yaml`
   - Lowercase, not `Config.yaml`

---

### Error: Assistant not discovered

**Symptom:**
After deployment, `osa myproject ask "test"` returns:
```
Error: Unknown command 'myproject'
```

**Cause:**
Assistant not registered in registry.

**Diagnosis:**

1. **Check discovery:**
   ```bash
   uv run python -c "from src.assistants import registry; print([a.id for a in registry.list_all()])"
   ```

2. **Check directory structure:**
   ```bash
   ls src/assistants/
   # Should show: myproject/
   ```

**Solution:**

1. **Ensure config.yaml exists:**
   ```bash
   ls src/assistants/myproject/config.yaml
   ```

2. **Restart server:**
   ```bash
   # Discovery happens at startup
   uv run uvicorn src.api.main:app --reload
   ```

3. **Check for validation errors:**
   ```bash
   uv run osa validate src/assistants/myproject/config.yaml
   ```

---

## Testing Issues

### Error: Tests fail with import errors

**Symptom:**
```
ImportError: cannot import name 'validate' from 'src.cli.validate'
```

**Cause:**
Module not in Python path or not installed.

**Solution:**

1. **Sync dependencies:**
   ```bash
   uv sync
   ```

2. **Run tests from repo root:**
   ```bash
   cd /path/to/osa
   uv run pytest tests/
   ```

3. **Check Python path:**
   ```bash
   uv run python -c "import sys; print(sys.path)"
   # Should include current directory
   ```

---

### Error: Tests fail with fixture errors

**Symptom:**
```
fixture 'tmp_path' not found
```

**Cause:**
Using old pytest version or fixture not available.

**Solution:**

1. **Update pytest:**
   ```bash
   uv sync --upgrade
   ```

2. **Verify pytest version:**
   ```bash
   uv run pytest --version
   # Should be >= 7.0
   ```

---

## Performance Issues

### Issue: Widget loads slowly

**Symptoms:**
- Widget takes 3-5+ seconds to appear
- First message slow to respond

**Causes:**
1. Large system prompt (too many preloaded docs)
2. Slow model
3. Network latency
4. Cold start (server sleeping)

**Solutions:**

**Reduce preloaded docs:**
```yaml
# Before - 5 preloaded docs = slow
documentation:
  - title: Doc 1
    preload: true
  - title: Doc 2
    preload: true
  # ... 3 more preloaded

# After - 1-2 critical docs only
documentation:
  - title: Core Spec
    preload: true
  - title: API Ref
    preload: false  # Fetch on-demand
```

**Use the faster model:**
```yaml
# Before - Sonnet 5 is the more capable of the two, and the slower
default_model: claude-sonnet-5

# After - Haiku 4.5, the platform default
default_model: claude-haiku-4-5
```

Extended thinking also costs latency before the first token.
Haiku thinks on a fixed budget and Sonnet decides per request, so a
thinking-heavy question is slower on either model than a lookup is.

**Check network:**
```bash
# Test API latency
time curl https://api.osc.earth/osa/health
# Should be < 1 second
```

---

### Issue: High API costs

**Symptoms:**
- AWS Marketplace bill higher than expected
- Usage exceeded budget

**Causes:**
1. `claude-sonnet-5` where `claude-haiku-4-5` would do
2. Long conversations (context accumulation)
3. Many users
4. Preloaded docs increasing prompt size
5. Prompt caching disabled, so the same system prompt is billed at full rate on every turn

**Solutions:**

**Use the cheaper model:**
```yaml
# Sonnet 5: twice Haiku's rate, worth it for genuinely hard questions
default_model: claude-sonnet-5

# Haiku 4.5: the default, and enough for documentation Q&A
default_model: claude-haiku-4-5
```

**Reduce preloaded docs:**
- Each preloaded doc adds to every request
- Move to on-demand retrieval
- Keep preloaded docs minimal

**Keep prompt caching on:**
- Cache reads bill at a tenth of the input rate, and the system prompt is the largest repeated part of a request
- A cache write costs more than an uncached read once, then pays for itself on the second turn

**Monitor usage:**
- `GET /{community_id}/metrics` reports `total_estimated_cost` from the same pricing table the platform bills against (admin or community key required)
- Set up budget alerts in AWS
- Track usage by community ID

**Cost Comparison:**
| Model | Input (per 1M tokens) | Output (per 1M tokens) | Use Case |
|-------|----------------------|------------------------|----------|
| `claude-haiku-4-5` | $1.00 | $5.00 | General Q&A, FAQ generation |
| `claude-sonnet-5` | $2.00 | $10.00 | Complex reasoning, long threads |

Opus is not offered here.
The platform exposes two models on purpose, so a community's cost is predictable and the fallback is always the cheaper one.

---

## Widget Integration Issues

### Issue: Widget appears but can't read page content

**Symptom:**
Assistant says "I cannot access the current page content" when asked about page.

**Cause:**
`enable_page_context` disabled or tool not available.

**Solution:**

```yaml
# Enable page context tool
enable_page_context: true
```

**Verify:**
```bash
# Check config
grep enable_page_context src/assistants/myproject/config.yaml
# Should show: enable_page_context: true
```

---

### Issue: Widget positioning problems

**Symptom:**
Widget icon overlaps with page content or appears in wrong location.

**Cause:**
CSS conflicts with your site's styles.

**Solution:**

**Add custom CSS:**
```html
<style>
  /* Adjust widget position */
  #osa-widget-container {
    bottom: 20px !important;
    right: 20px !important;
    z-index: 9999 !important;
  }
</style>
```

**Check for conflicts:**
```javascript
// In browser console
console.log(getComputedStyle(document.getElementById('osa-widget-container')));
```

---

## Documentation Sync Issues

### Error: Documentation fetch fails

**Symptom:**
Assistant says "I couldn't retrieve that documentation."

**Causes:**
1. `source_url` unreachable
2. GitHub rate limit
3. URL changed/moved

**Diagnosis:**

```bash
# Test URL directly
curl -I https://raw.githubusercontent.com/org/repo/main/docs.md
# Should return 200 OK
```

**Solutions:**

**URL moved:**
```yaml
# Update to new URL
documentation:
  - title: My Doc
    url: https://newsite.org/docs
    source_url: https://raw.githubusercontent.com/org/repo/main/docs/newpath.md
```

**GitHub rate limit:**
- Wait an hour for limit reset
- Use GitHub token for higher limits
- Move docs to CDN

**HTTPS required:**
```yaml
# Wrong - HTTP not secure
source_url: http://example.com/docs.md

# Correct - HTTPS
source_url: https://example.com/docs.md
```

---

## Getting Help

If you're still stuck after trying these solutions:

1. **Check logs:**
   ```bash
   # Local development
   uv run uvicorn src.api.main:app --reload
   # Watch for errors in output

   # Production
   docker logs osa-prod
   ```

2. **Run health check:**
   ```bash
   uv run osa health
   ```

3. **Validate config again:**
   ```bash
   uv run osa validate src/assistants/your-community/config.yaml --test-api-key
   ```

4. **File an issue:**
   - GitHub: https://github.com/OpenScience-Collective/osa/issues
   - Include:
     - Error message (full text)
     - Config file (sanitized, remove API keys!)
     - Steps to reproduce
     - Environment (OS, Python version)

5. **Ask in discussions:**
   - https://github.com/OpenScience-Collective/osa/discussions

---

## Prevention Checklist

Before deploying to production:

- [ ] Config validated locally (`osa validate`)
- [ ] API key tested (`--test-api-key`)
- [ ] CORS origins match production domains
- [ ] Documentation URLs verified (returns 200 OK)
- [ ] Widget tested on actual website
- [ ] Costs estimated based on expected usage
- [ ] Monitoring/alerts configured
- [ ] Team trained on troubleshooting basics

---

## Common Error Messages Reference

**Quick lookup table:**

| Error | Section | Quick Fix |
|-------|---------|-----------|
| YAML syntax error | [Config Validation](#error-yaml-syntax-error) | Check indentation, quotes |
| kebab-case | [Config Validation](#error-community-id-must-be-kebab-case) | Use lowercase with hyphens |
| Invalid CORS origin | [Config Validation](#error-invalid-cors-origin) | Add `https://` prefix |
| preload requires source_url | [Config Validation](#error-preload-requires-source_url) | Add `source_url` field |
| API key not set | [API Keys](#warning-api-key-env-var-not-set) | Export env var |
| 401 Unauthorized | [API Keys](#error-api-key-test-failed-401-unauthorized) | Check API key validity |
| CORS blocked | [Runtime](#error-cors-policy-blocked) | Add origin to config |
| Widget not loading | [Runtime](#error-widget-not-loading) | Check script, community ID |
| Config not found | [Deployment](#error-config-file-not-found) | Check file path |
| Assistant not discovered | [Deployment](#error-assistant-not-discovered) | Restart server |
