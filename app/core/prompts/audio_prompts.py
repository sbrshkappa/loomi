"""
Audio-specific story generation prompts.
This module contains enhanced prompts optimized for audio narration.
"""

# Import base prompts for modular composition
from app.core.prompts.base_prompts import BASE_STORY_PROMPT
from app.core.prompts.image_prompts import IMAGE_GENERATION_PROMPT

# Audio-specific enhancements (to be added to base story prompt)
AUDIO_ENHANCEMENTS = """
When creating stories for audio narration, focus on these key principles:

**AUDIO-FIRST STORYTELLING TECHNIQUES:**

1. **Rich Sensory Details**: Include vivid descriptions that engage all five senses:
   - What things look like (colors, shapes, textures)
   - What things sound like (rustling leaves, bubbling brooks, gentle footsteps)
   - What things feel like (soft fur, warm sunlight, cool breeze)
   - What things smell like (fresh bread, flowers, rain)
   - What things taste like (sweet honey, warm soup)

2. **Emotional Expression**: Make emotions palpable through:
   - Character voice changes and expressions
   - Emotional reactions and body language
   - Heartfelt dialogue and inner thoughts
   - Mood-setting descriptions

3. **Rhythm and Pacing**: Create natural speech patterns with:
   - Varied sentence lengths for rhythm
   - Repetition for emphasis and memory
   - Pauses and breaks for dramatic effect
   - Flowing transitions between scenes

4. **Character Voices**: Give each character distinct personality through:
   - Unique speech patterns and vocabulary
   - Character-specific expressions and mannerisms
   - Emotional states reflected in their dialogue
   - Age-appropriate language for each character

5. **Immersive Settings**: Paint vivid pictures with:
   - Detailed environmental descriptions
   - Atmospheric details (lighting, weather, time of day)
   - Interactive elements (objects characters touch, move, or use)
   - Spatial relationships and movement

**STORY STRUCTURE FOR AUDIO:**

- **Opening Hook**: Start with an engaging moment or question that draws listeners in
- **Character Introduction**: Introduce characters with rich, memorable details
- **Problem/Challenge**: Present a clear conflict or adventure
- **Journey/Development**: Show characters growing and changing
- **Resolution**: Provide a satisfying, positive conclusion
- **Closing**: End with a warm, comforting moment

**LANGUAGE GUIDELINES:**

- Use simple but evocative vocabulary
- Include onomatopoeia (sound words) when appropriate
- Create memorable phrases and expressions
- Use dialogue to advance the story and reveal character
- Include gentle humor and warmth
- Avoid complex sentence structures that are hard to follow when spoken

**EMOTIONAL ENGAGEMENT:**

- Create moments of wonder and discovery
- Include gentle suspense and anticipation
- Show characters overcoming fears or challenges
- Celebrate friendship, kindness, and courage
- End with feelings of comfort and security

**AGE-APPROPRIATE CONTENT:**

- For ages 2-5: Simple plots, lots of repetition, familiar objects
- For ages 5-8: More complex characters, gentle adventures, clear morals
- For ages 8-12: Deeper character development, more sophisticated plots
- Always maintain positive, uplifting themes

**AUDIO-SPECIFIC ENHANCEMENTS:**

- Include natural pauses and breathing spaces
- Create opportunities for different voices and expressions
- Add sound effects through descriptive language
- Use rhythm and repetition for memorable moments
- Include interactive elements that encourage listener participation

**AGE-BASED STORY LENGTH FOR AUDIO:**

- For children below 3 years: 2-3 minutes (150-200 words)
- For ages 3-7: 3-5 minutes (300-500 words)
- For ages 7-12: 5-8 minutes (500-800 words)
- For ages above 12: 8-12 minutes (800-1200 words)

Remember: Your story will be read aloud, so every word should sound beautiful when spoken. Create a rich, immersive experience that captivates young listeners and makes them feel like they're right there in the story world.
"""

# Audio-specific storybook generation enhancements
AUDIO_STORYBOOK_ENHANCEMENTS = """
When the user requests an audio storybook, create a rich, detailed story optimized for audio narration. 

**AUDIO STORYBOOK REQUIREMENTS:**

1. **Enhanced Descriptions**: Include more sensory details than a regular story:
   - Sound descriptions (rustling, whispering, thumping, etc.)
   - Texture and touch details
   - Smell and taste elements
   - Visual details that paint vivid pictures

2. **Character Development**: Give each character:
   - Distinct voice patterns and speech habits
   - Emotional depth and personality quirks
   - Physical descriptions that help listeners visualize
   - Motivations and feelings that drive their actions

3. **Atmospheric Elements**: Create immersive environments with:
   - Weather and lighting descriptions
   - Background sounds and ambient noise
   - Time of day and seasonal details
   - Emotional atmosphere and mood

4. **Dialogue Enhancement**: Make conversations:
   - Natural and flowing
   - Character-specific in vocabulary and style
   - Emotionally expressive
   - Age-appropriate but engaging

5. **Narrative Pacing**: Structure the story with:
   - Clear scene transitions
   - Natural pauses and breaks
   - Varied sentence rhythms
   - Building tension and release

**STORYBOOK STRUCTURE FOR AUDIO:**

Break the story into logical sections that work well for audio narration:

1. **Title**: Create an engaging, memorable title
2. **Characters**: Rich descriptions of all characters
3. **Cover Description**: A vivid scene that captures the story's essence
4. **Pages**: Each page should be a complete scene or moment that flows naturally when read aloud

**PAGE CONTENT GUIDELINES:**

- Each page should be 1-2 paragraphs that can be read in 30-60 seconds
- Include rich sensory details and emotional content
- Use dialogue to advance the plot and reveal character
- Create clear visual and emotional scenes
- End each page with a natural pause or transition

**AUDIO-SPECIFIC ENHANCEMENTS:**

- Include onomatopoeia and sound words
- Add emotional expressions and reactions
- Create opportunities for different voices
- Include gentle humor and warmth
- Use repetition for emphasis and memory
- Add interactive elements that encourage listener participation

Generate the storybook in JSON format with detailed character descriptions, rich page content, and vivid image descriptions that will create an immersive audio experience.
"""

# Composable prompt combinations for different output types
AUDIO_STORY_PROMPT = BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS
AUDIO_STORYBOOK_PROMPT = BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + AUDIO_STORYBOOK_ENHANCEMENTS + IMAGE_GENERATION_PROMPT

# For future use: Audio + Images combination
AUDIO_AND_IMAGES_PROMPT = BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + IMAGE_GENERATION_PROMPT 