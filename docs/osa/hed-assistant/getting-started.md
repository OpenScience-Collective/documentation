# Getting Started

This guide will help you set up and start using the HED Assistant.

## Prerequisites

- Python 3.11 or higher
- pip or uv package manager

## Installation

### From PyPI (Recommended)

```bash
pip install hed-assistant
```

### From Source

```bash
git clone https://github.com/OpenScience-Collective/hed-assistant
cd hed-assistant
pip install -e .
```

### Using uv

```bash
uv pip install hed-assistant
```

## Configuration

### Basic Setup

After installation, configure the HED Assistant:

```python
from hed_assistant import HEDAssistant

# Initialize with default settings
assistant = HEDAssistant()

# Or specify a HED schema version
assistant = HEDAssistant(schema_version="8.2.0")
```

### Environment Variables

You can configure the assistant using environment variables:

```bash
export HED_SCHEMA_VERSION="8.2.0"
export HED_ASSISTANT_CACHE_DIR="~/.cache/hed-assistant"
```

## Verifying Installation

Test that everything is working:

```python
from hed_assistant import HEDAssistant

assistant = HEDAssistant()
print(assistant.version)
print(assistant.schema_version)
```

## Next Steps

- Read the [Usage Guide](usage.md) to learn how to annotate with HED
- Explore the [API Reference](api.md) for programmatic access
- Check out examples in the repository
