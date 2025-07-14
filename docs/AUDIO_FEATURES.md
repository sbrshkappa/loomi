# Audio-Optimized Story Generation Features

## Overview

Loomi now includes enhanced audio-optimized story generation that creates richer, more detailed content perfect for audio narration. These features are designed to make stories come alive when read aloud, with enhanced sensory details, emotional expressions, and natural speech patterns.

## New Features

### 1. Audio-Optimized Prompts

We've created specialized prompts that generate content specifically designed for audio narration:

- **Rich Sensory Details**: Stories include vivid descriptions of sounds, textures, smells, and visual elements
- **Emotional Expression**: Characters have distinct voices and emotional depth
- **Natural Speech Patterns**: Content flows naturally when spoken aloud
- **Immersive Settings**: Detailed atmospheric descriptions create vivid mental pictures
- **Interactive Elements**: Stories encourage listener participation and engagement

### 2. New API Endpoints

#### Audio Chat Endpoint
```
POST /api/v1/audio-chat
```

This endpoint uses audio-optimized prompts to generate stories that are perfect for narration.

**Example Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Tell me a story about a brave little mouse who goes on an adventure"
    }
  ],
  "session_id": "optional-session-id"
}
```

#### Enhanced Audio Storybook Generation
```
POST /api/v1/storybook
```

The existing storybook endpoint now includes enhanced audio processing when `output_type` is set to `"audio"`.

**Example Request:**
```json
{
  "title": "The Brave Little Mouse",
  "characters": [
    {
      "character_name": "Mickey",
      "character_features": "A small brown mouse with big ears and a brave heart"
    }
  ],
  "cover_picture_description": "A brave little mouse standing on a cheese",
  "num_pages": 3,
  "pages": [
    {
      "page_num": 1,
      "page_text": "Once upon a time, in a cozy little burrow...",
      "page_picture_description": "A cozy mouse hole"
    }
  ],
  "output_type": "audio"
}
```

## Key Differences: Regular vs Audio-Optimized Stories

### Regular Story Generation
- Focused on visual reading
- Standard descriptive language
- Basic character development
- Traditional story structure

### Audio-Optimized Story Generation
- **Enhanced Sensory Details**: 
  - Sound descriptions (rustling leaves, bubbling brooks)
  - Texture and touch details
  - Smell and taste elements
  - Rich visual descriptions

- **Emotional Depth**:
  - Character voice patterns and speech habits
  - Emotional reactions and body language
  - Heartfelt dialogue and inner thoughts
  - Mood-setting descriptions

- **Natural Speech Patterns**:
  - Varied sentence lengths for rhythm
  - Repetition for emphasis and memory
  - Natural pauses and breaks
  - Flowing transitions

- **Immersive Atmosphere**:
  - Weather and lighting descriptions
  - Background sounds and ambient noise
  - Time of day and seasonal details
  - Interactive elements

## Testing the Audio Features

### Run the Test Script
```bash
python test_audio_prompts.py
```

This script demonstrates the difference between regular and audio-optimized story generation.

### Manual Testing

1. **Test Audio Chat:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/audio-chat" \
        -H "Content-Type: application/json" \
        -d '{
          "messages": [
            {
              "role": "user",
              "content": "Tell me a story about a magical forest"
            }
          ]
        }'
   ```

2. **Test Audio Storybook:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/storybook" \
        -H "Content-Type: application/json" \
        -d '{
          "title": "The Magical Forest Adventure",
          "characters": [
            {
              "character_name": "Luna",
              "character_features": "A curious fox with silver fur and bright green eyes"
            }
          ],
          "cover_picture_description": "A magical forest with glowing mushrooms",
          "num_pages": 2,
          "pages": [
            {
              "page_num": 1,
              "page_text": "In a forest where the trees whispered ancient secrets...",
              "page_picture_description": "A mystical forest clearing"
            },
            {
              "page_num": 2,
              "page_text": "Luna discovered a hidden path...",
              "page_picture_description": "A glowing path through the forest"
            }
          ],
          "output_type": "audio"
        }'
   ```

## Audio-Specific Enhancements

### Story Length Guidelines for Audio
- **Ages 2-5**: 2-3 minutes (150-200 words)
- **Ages 5-8**: 3-5 minutes (300-500 words)
- **Ages 7-12**: 5-8 minutes (500-800 words)
- **Ages 12+**: 8-12 minutes (800-1200 words)

### Audio Narration Features
- Warm introductions and closings
- Natural page transitions
- Character voice distinctions
- Emotional expression cues
- Interactive listener engagement
- Sound effect descriptions
- Rhythmic language patterns

## Integration with OpenVoice V2

The audio-optimized stories work seamlessly with the existing OpenVoice V2 and MeloTTS integration:

1. Generate an audio-optimized story using the new endpoints
2. The enhanced text is automatically processed by the audio generator
3. OpenVoice V2 creates expressive, emotionally rich narration
4. The result is a high-quality audio storybook

## Best Practices

### For Audio Story Generation
1. **Ask for the child's age** to tailor content appropriately
2. **Include character details** to help with voice generation
3. **Specify the setting** for atmospheric enhancement
4. **Request emotional themes** for better expression

### For Audio Narration
1. **Use the audio-chat endpoint** for interactive story creation
2. **Request audio storybooks** for complete narrated experiences
3. **Test different story types** to explore the range of audio enhancements
4. **Combine with visual elements** for multimedia experiences

## Future Enhancements

- Voice character mapping for different characters
- Background music and sound effects
- Multi-language audio support
- Interactive audio elements
- Audio story templates and themes 