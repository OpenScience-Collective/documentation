# Usage Guide

This guide covers common use cases for the HED Assistant.

## Basic Annotation

### Creating HED Strings

```python
from hed_assistant import HEDAssistant

assistant = HEDAssistant()

# Get suggestions for an event description
event = "participant pressed the left button"
suggestions = assistant.suggest(event)

for suggestion in suggestions:
    print(f"{suggestion.tag}: {suggestion.confidence:.2f}")
```

### Validating HED Strings

```python
# Validate a HED string
hed_string = "Sensory-event, Visual-presentation"
result = assistant.validate(hed_string)

if result.is_valid:
    print("Valid HED string!")
else:
    for error in result.errors:
        print(f"Error: {error.message}")
```

## Working with Events

### Annotating Event Files

```python
import pandas as pd
from hed_assistant import HEDAssistant

assistant = HEDAssistant()

# Load your events file
events = pd.read_csv("events.tsv", sep="\t")

# Generate annotations for each event
annotations = []
for _, row in events.iterrows():
    suggestion = assistant.suggest(row["trial_type"])[0]
    annotations.append(suggestion.tag)

events["HED"] = annotations
events.to_csv("events_annotated.tsv", sep="\t", index=False)
```

### Batch Processing

```python
# Process multiple descriptions at once
descriptions = [
    "visual stimulus onset",
    "button press response",
    "feedback presentation"
]

results = assistant.suggest_batch(descriptions)

for desc, suggestions in zip(descriptions, results):
    print(f"{desc}: {suggestions[0].tag}")
```

## Schema Exploration

### Browsing Tags

```python
# Search for tags
results = assistant.search_schema("visual")

for tag in results:
    print(f"{tag.name}: {tag.description}")
```

### Getting Tag Details

```python
# Get detailed information about a tag
tag_info = assistant.get_tag("Visual-presentation")

print(f"Name: {tag_info.name}")
print(f"Description: {tag_info.description}")
print(f"Parent: {tag_info.parent}")
print(f"Children: {tag_info.children}")
```

## Integration with BIDS

### Working with BIDS Datasets

```python
from hed_assistant import HEDAssistant
from hed_assistant.bids import BIDSDataset

assistant = HEDAssistant()
dataset = BIDSDataset("/path/to/bids/dataset")

# Annotate all events files
for events_file in dataset.events_files:
    annotations = assistant.annotate_events(events_file)
    events_file.save_with_hed(annotations)
```

## Tips and Best Practices

1. **Start Specific** - Use the most specific HED tags that apply
2. **Validate Often** - Check your annotations regularly
3. **Use Definitions** - Create definitions for repeated patterns
4. **Document Choices** - Keep notes on annotation decisions
