# API Reference

This page documents the HED Assistant Python API.

## HEDAssistant

The main class for interacting with the HED Assistant.

### Constructor

```python
class HEDAssistant:
    def __init__(
        self,
        schema_version: str | None = None,
        cache_dir: str | Path | None = None,
    ) -> None:
        """
        Initialize the HED Assistant.

        Args:
            schema_version: HED schema version to use (default: latest)
            cache_dir: Directory for caching schema files
        """
```

### Properties

#### `version`

```python
@property
def version(self) -> str:
    """Return the HED Assistant version."""
```

#### `schema_version`

```python
@property
def schema_version(self) -> str:
    """Return the currently loaded HED schema version."""
```

### Methods

#### `suggest`

```python
def suggest(
    self,
    description: str,
    top_k: int = 5,
    threshold: float = 0.5,
) -> list[Suggestion]:
    """
    Get HED tag suggestions for an event description.

    Args:
        description: Natural language description of the event
        top_k: Maximum number of suggestions to return
        threshold: Minimum confidence threshold

    Returns:
        List of Suggestion objects sorted by confidence
    """
```

#### `suggest_batch`

```python
def suggest_batch(
    self,
    descriptions: list[str],
    top_k: int = 5,
    threshold: float = 0.5,
) -> list[list[Suggestion]]:
    """
    Get HED tag suggestions for multiple descriptions.

    Args:
        descriptions: List of event descriptions
        top_k: Maximum number of suggestions per description
        threshold: Minimum confidence threshold

    Returns:
        List of suggestion lists, one per description
    """
```

#### `validate`

```python
def validate(
    self,
    hed_string: str,
    check_warnings: bool = True,
) -> ValidationResult:
    """
    Validate a HED string.

    Args:
        hed_string: HED string to validate
        check_warnings: Include warnings in results

    Returns:
        ValidationResult with validity status and any errors
    """
```

#### `search_schema`

```python
def search_schema(
    self,
    query: str,
    limit: int = 20,
) -> list[TagInfo]:
    """
    Search the HED schema for matching tags.

    Args:
        query: Search query string
        limit: Maximum results to return

    Returns:
        List of matching TagInfo objects
    """
```

#### `get_tag`

```python
def get_tag(self, tag_name: str) -> TagInfo:
    """
    Get detailed information about a HED tag.

    Args:
        tag_name: Name of the tag

    Returns:
        TagInfo object with tag details

    Raises:
        TagNotFoundError: If tag doesn't exist in schema
    """
```

---

## Data Classes

### Suggestion

```python
@dataclass
class Suggestion:
    """A HED tag suggestion."""

    tag: str
    """The suggested HED tag string."""

    confidence: float
    """Confidence score between 0 and 1."""

    explanation: str | None
    """Optional explanation for the suggestion."""
```

### ValidationResult

```python
@dataclass
class ValidationResult:
    """Result of HED string validation."""

    is_valid: bool
    """Whether the HED string is valid."""

    errors: list[ValidationError]
    """List of validation errors."""

    warnings: list[ValidationWarning]
    """List of validation warnings."""
```

### TagInfo

```python
@dataclass
class TagInfo:
    """Information about a HED tag."""

    name: str
    """Tag name."""

    description: str
    """Tag description."""

    parent: str | None
    """Parent tag name."""

    children: list[str]
    """List of child tag names."""

    attributes: dict[str, Any]
    """Tag attributes from schema."""
```

---

## Exceptions

### `HEDAssistantError`

Base exception for all HED Assistant errors.

### `TagNotFoundError`

Raised when a requested tag doesn't exist in the schema.

### `ValidationError`

Raised when validation fails unexpectedly.

### `SchemaLoadError`

Raised when the HED schema cannot be loaded.
