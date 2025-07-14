# Flexible Prompt Architecture

## Overview

Loomi now features a **modular, composable prompt architecture** that allows for flexible story generation with different output types. This architecture separates concerns and enables easy combination of story generation, audio enhancements, and image generation.

## Architecture Components

### 1. Base Components

- **`base_prompts.py`**: Contains `BASE_STORY_PROMPT` - the core story generation logic
- **`image_prompts.py`**: Contains `IMAGE_GENERATION_PROMPT` - image generation instructions
- **`audio_prompts.py`**: Contains audio enhancements (`AUDIO_ENHANCEMENTS`, `AUDIO_STORYBOOK_ENHANCEMENTS`)

### 2. Prompt Factory

- **`prompt_factory.py`**: Provides easy access to different prompt combinations
- **`PromptFactory`**: Class for creating prompt combinations
- **Convenience functions**: Easy-to-use functions for each output type

### 3. Legacy Support

- **`story_prompts.py`**: Maintains backward compatibility by combining base + image prompts

## Available Output Types

| Output Type | Description | Components Used |
|-------------|-------------|-----------------|
| `text` | Basic story generation (text only) | `BASE_STORY_PROMPT` |
| `pdf` | Traditional storybook with images | `BASE_STORY_PROMPT + IMAGE_GENERATION_PROMPT` |
| `audio` | Audio-optimized story (audio only) | `BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS` |
| `audio_pdf` | Audio-optimized story with images | `BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + IMAGE_GENERATION_PROMPT` |
| `audio_storybook` | Enhanced audio storybook | `BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + AUDIO_STORYBOOK_ENHANCEMENTS + IMAGE_GENERATION_PROMPT` |

## Usage Examples

### 1. Using the Prompt Factory

```python
from app.core.prompts.prompt_factory import PromptFactory

# Get different prompt combinations
text_prompt = PromptFactory.get_prompt("text")
pdf_prompt = PromptFactory.get_prompt("pdf")
audio_prompt = PromptFactory.get_prompt("audio")
audio_pdf_prompt = PromptFactory.get_prompt("audio_pdf")
audio_storybook_prompt = PromptFactory.get_prompt("audio_storybook")
```

### 2. Using Convenience Functions

```python
from app.core.prompts.prompt_factory import (
    get_text_prompt,
    get_pdf_prompt,
    get_audio_prompt,
    get_audio_pdf_prompt,
    get_audio_storybook_prompt
)

# Get prompts directly
text_prompt = get_text_prompt()
pdf_prompt = get_pdf_prompt()
audio_prompt = get_audio_prompt()
```

### 3. API Usage

#### Flexible Story Endpoint
```bash
# Text-only story
curl -X POST "http://localhost:8000/api/v1/story?output_type=text" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Tell me a story about a brave mouse"}]}'

# Audio-optimized story
curl -X POST "http://localhost:8000/api/v1/story?output_type=audio" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Tell me a story about a brave mouse"}]}'

# Audio + Images storybook
curl -X POST "http://localhost:8000/api/v1/story?output_type=audio_pdf" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Tell me a story about a brave mouse"}]}'
```

#### Legacy Endpoints (Still Available)
```bash
# Traditional PDF storybook
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Tell me a story about a brave mouse"}]}'

# Audio-optimized storybook
curl -X POST "http://localhost:8000/api/v1/audio-chat" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Tell me a story about a brave mouse"}]}'
```

## Key Benefits

### 1. **Modularity**
- Each component has a single responsibility
- Easy to modify or extend individual components
- No code duplication

### 2. **Flexibility**
- Mix and match components as needed
- Easy to add new output types
- Backward compatibility maintained

### 3. **Maintainability**
- Clear separation of concerns
- Easy to test individual components
- Simple to understand and modify

### 4. **Extensibility**
- Easy to add new enhancement types (video, interactive, etc.)
- Simple to create new prompt combinations
- Future-proof architecture

## Component Details

### Base Story Prompt (`BASE_STORY_PROMPT`)
- Core story generation logic
- Character development guidelines
- Age-appropriate content rules
- Conversation flow management
- Story structure requirements

### Audio Enhancements (`AUDIO_ENHANCEMENTS`)
- Rich sensory details (sounds, textures, smells)
- Emotional expression guidelines
- Rhythm and pacing instructions
- Character voice distinctions
- Interactive elements for listeners

### Image Generation (`IMAGE_GENERATION_PROMPT`)
- Character description guidelines
- Page layout instructions
- Visual detail requirements
- Image description examples
- JSON output formatting

### Audio Storybook Enhancements (`AUDIO_STORYBOOK_ENHANCEMENTS`)
- Audio-specific storybook structure
- Page content guidelines for narration
- Enhanced dialogue requirements
- Audio pacing instructions

## Future Enhancements

### Easy to Add New Types
```python
# Example: Adding video support
VIDEO_ENHANCEMENTS = """
Video-specific enhancements...
"""

# Add to PromptFactory
elif output_type == "video":
    return BASE_STORY_PROMPT + VIDEO_ENHANCEMENTS + IMAGE_GENERATION_PROMPT
```

### Easy to Add New Components
```python
# Example: Adding interactive elements
INTERACTIVE_ENHANCEMENTS = """
Interactive story elements...
"""

# Combine as needed
interactive_audio_pdf = BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + INTERACTIVE_ENHANCEMENTS + IMAGE_GENERATION_PROMPT
```

## Migration Guide

### For Existing Code
- **No changes needed** - legacy endpoints still work
- **Optional upgrade** - use new flexible endpoints for more control
- **Gradual migration** - update endpoints one at a time

### For New Features
- Use `PromptFactory` for new prompt combinations
- Leverage modular components for custom needs
- Follow the composable pattern for consistency

## Testing

### Test Different Output Types
```python
# Test script to verify all output types
from app.core.prompts.prompt_factory import PromptFactory, AVAILABLE_OUTPUT_TYPES

for output_type in AVAILABLE_OUTPUT_TYPES:
    prompt = PromptFactory.get_prompt(output_type)
    print(f"{output_type}: {len(prompt)} characters")
```

### Verify Backward Compatibility
```python
# Ensure legacy imports still work
from app.core.prompts.story_prompts import SYSTEM_PROMPT
from app.core.prompts.audio_prompts import AUDIO_STORY_PROMPT
```

This architecture provides maximum flexibility while maintaining simplicity and backward compatibility! 🎯✨ 