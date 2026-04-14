# OSC Documentation

Documentation site for the Open Science Collective (OSC), built with MkDocs Material.

## Two Documentation Sources

This repo serves two independent MkDocs sites from two config files, each deploying to its own subdomain:

| Config | docs_dir | Subdomain | Content |
|--------|----------|-----------|---------|
| `mkdocs.yml` | `docs/` | docs.osc.earth | OSC and OSA documentation |
| `mkdocs-courses.yml` | `courses/` | courses.osc.earth | Course materials |

Both share the `overrides/` directory for theme customizations.

## Build and Serve

```bash
# Main docs
uv run mkdocs serve                          # dev server (docs.osc.earth)
uv run mkdocs build                          # build to site/

# Courses
uv run mkdocs serve -f mkdocs-courses.yml    # dev server (courses.osc.earth)
uv run mkdocs build -f mkdocs-courses.yml    # build to site-courses/
```

## OS-Specific Tabs

Both sites use `content.tabs.link` (Material for MkDocs), which syncs tab selections across the page and persists the choice in localStorage. For this to work, all OS tab groups must use exactly these labels:

- `=== "macOS"`
- `=== "Linux"`
- `=== "Windows"`

Never use combined labels like "macOS / Linux" or qualified labels like "macOS: Homebrew"; they break cross-group syncing.

## Submodules

- `osa/` -- the [OSA application repo](https://github.com/OpenScience-Collective/osa) (git submodule). Not part of the docs build; used for API reference generation when enabled.
