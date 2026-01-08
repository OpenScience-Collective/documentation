# Open Science Collective Documentation

Documentation for the [Open Science Collective](https://osc.earth) and its projects, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Bun](https://bun.sh/) (for scripts)
- [Wrangler](https://developers.cloudflare.com/workers/wrangler/) (for Cloudflare deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/OpenScience-Collective/documentation
cd documentation

# Install dependencies
uv sync
```

### Local Development

```bash
# Start the development server
bun run dev
# or
uv run mkdocs serve
```

Visit `http://localhost:8000` to view the documentation.

### Building

```bash
# Build static site
bun run build
# or
uv run mkdocs build
```

### Deployment

Deploy to Cloudflare Pages:

```bash
bun run deploy
```

This builds the site and deploys to `osc-docs.pages.dev`.

## Structure

```
documentation/
├── docs/                    # Markdown source files
│   ├── index.md            # Homepage
│   ├── collective/         # Collective documentation
│   │   ├── about.md
│   │   ├── mission.md
│   │   └── contributing.md
│   └── osa/                # OSA projects
│       └── hed-assistant/  # HED Assistant docs
├── overrides/              # Theme customizations
├── mkdocs.yml              # MkDocs configuration
├── pyproject.toml          # Python dependencies
├── package.json            # Bun scripts
└── wrangler.toml           # Cloudflare Pages config
```

## License

BSD-3-Clause - see [LICENSE](LICENSE) for details.
