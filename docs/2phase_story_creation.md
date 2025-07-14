# 2-Phase Story Creation API

This document describes the new 2-phase story creation approach that makes story generation more engaging and interactive for children.

## Overview

The 2-phase approach separates story creation into two distinct phases:

1. **Phase 1: Interactive Planning** - Collaborative story development
2. **Phase 2: Story Generation** - Final story creation in desired format

This approach creates a more engaging, child-friendly experience where children can actively participate in creating their own stories.

## Phase 1: Interactive Story Planning

### Endpoint: `POST /api/v1/plan-story`

**Purpose**: Engage in a conversational planning session to develop story ideas collaboratively.

**Features**:
- Child-friendly, enthusiastic AI assistant ("Story Buddy")
- One question at a time to avoid overwhelming children
- Builds on children's ideas and encourages creativity
- Maintains conversation context throughout the session
- Age-appropriate questions and suggestions

### Request Format

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I want to create a story about a little girl who discovers a magical garden"
    }
  ],
  "session_id": "optional-session-id"
}
```

### Response Format

```json
{
  "response": "Oh, that sounds like such an exciting adventure! 🌸 A magical garden! I love that idea! What should we call our amazing little girl? And how old is she?",
  "session_id": "abc123def456",
  "output_type": "planning"
}
```

### Example Planning Conversation

**User**: "I want to create a story about a little girl who discovers a magical garden"

**AI**: "Oh, that sounds like such an exciting adventure! 🌸 A magical garden! I love that idea! What should we call our amazing little girl? And how old is she?"

**User**: "Her name is Lily and she's 5 years old. She loves flowers and animals."

**AI**: "Lily! What a beautiful name! 🌺 And 5 years old - perfect age for magical adventures! Since Lily loves flowers and animals, what if the magical garden has special talking flowers? What color should her favorite flower be?"

**User**: "Pink roses! And maybe there's a wise old tree too."

**AI**: "Pink roses that can talk! 🌹 That's so magical! And a wise old tree - I love that! What should the tree's name be? And what exciting challenge should Lily face in the garden?"

### Planning Session Management

- **Session Persistence**: All planning conversations are saved and can be continued
- **Context Awareness**: AI remembers all previous details and builds upon them
- **Flexible Duration**: Planning can continue until the child is satisfied
- **Natural Transitions**: AI suggests moving to story generation when ready

## Phase 2: Story Generation

### Endpoint: `POST /api/v1/generate-story`

**Purpose**: Generate the final story from the planning session in the desired format.

**Features**:
- Uses all planning conversation context
- Generates story optimized for the chosen output type
- Supports multiple output formats (audio, PDF, text, etc.)
- Maintains consistency with planning decisions

### Request Format

```bash
POST /api/v1/generate-story?session_id=abc123def456&output_type=audio
```

**Query Parameters**:
- `session_id` (required): Session ID from planning phase
- `output_type` (optional, default: "audio"): Desired output format

### Available Output Types

- `"text"`: Basic story text
- `"pdf"`: Illustrated storybook PDF
- `"audio"`: Audio narration (MP3)
- `"audio_pdf"`: Audio + PDF combination
- `"audio_storybook"`: Enhanced audio storybook

### Response Format

```json
{
  "response": "### **Lily's Magical Garden Adventure**\n\nOnce upon a time, in a cozy little house...",
  "audio_url": "/api/v1/audio/story_abc123.mp3",
  "storybook_name": null,
  "session_id": "abc123def456",
  "output_type": "audio"
}
```

## Complete Workflow Example

### Step 1: Start Planning Session

```bash
curl -X POST "http://localhost:8000/api/v1/plan-story" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "I want to create a story about a brave little mouse"
      }
    ]
  }'
```

### Step 2: Continue Planning (multiple interactions)

```bash
curl -X POST "http://localhost:8000/api/v1/plan-story" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "His name is Max and he loves cheese"
      }
    ],
    "session_id": "abc123def456"
  }'
```

### Step 3: Generate Final Story

```bash
curl -X POST "http://localhost:8000/api/v1/generate-story?session_id=abc123def456&output_type=audio"
```

### Step 4: Download Audio

```bash
curl -O "http://localhost:8000/api/v1/audio/story_abc123.mp3"
```

## Session Management

### Get Session History

```bash
GET /api/v1/sessions/{session_id}/history
```

### Delete Session

```bash
DELETE /api/v1/sessions/{session_id}
```

## Benefits of 2-Phase Approach

### For Children
- **Active Participation**: Children feel like they're creating the story
- **Building Excitement**: Planning builds anticipation for the final story
- **Learning Opportunity**: Develops creativity and storytelling skills
- **Personal Connection**: Stories feel more personal and meaningful

### For Parents/Educators
- **Quality Time**: Interactive planning creates bonding opportunities
- **Educational Value**: Teaches story structure and creative thinking
- **Customization**: Stories can be tailored to child's interests and needs
- **Engagement**: Keeps children interested throughout the process

### For Developers
- **Better Context**: Planning provides rich context for story generation
- **Higher Quality**: More detailed, personalized stories
- **Flexible Output**: Same planning can generate multiple formats
- **Session Management**: Persistent conversations for complex stories

## Comparison: 2-Phase vs Direct Generation

| Aspect | Direct Generation | 2-Phase Approach |
|--------|------------------|------------------|
| **Engagement** | One-shot interaction | Extended, interactive experience |
| **Personalization** | Limited to initial prompt | Rich, detailed personalization |
| **Child Involvement** | Passive consumption | Active participation |
| **Story Quality** | Good | Excellent (more context) |
| **Educational Value** | Low | High (teaches storytelling) |
| **Time Investment** | Quick | Longer but more rewarding |

## Best Practices

### For Planning Sessions
1. **Start Simple**: Begin with basic story ideas
2. **Build Gradually**: Add details one at a time
3. **Encourage Creativity**: Praise and build on child's ideas
4. **Be Patient**: Let children think and respond
5. **Natural Flow**: Allow conversation to develop organically

### For Story Generation
1. **Choose Appropriate Format**: Consider child's age and preferences
2. **Use Planning Context**: Ensure final story reflects planning decisions
3. **Quality Check**: Review generated content for appropriateness
4. **Multiple Formats**: Consider generating multiple formats from same planning

## Error Handling

### Common Issues
- **Session Not Found**: Ensure planning session exists before generation
- **Invalid Output Type**: Use supported output types only
- **Audio Generation Failures**: Check audio service dependencies
- **Planning Timeout**: Long planning sessions may timeout

### Troubleshooting
1. **Check Session ID**: Verify session exists and is valid
2. **Validate Output Type**: Use correct output type parameter
3. **Monitor Audio Service**: Ensure OpenVoice and MeloTTS are working
4. **Review Planning**: Ensure sufficient planning context exists

## Future Enhancements

### Planned Features
- **Visual Planning**: Add image-based planning options
- **Character Creation**: Dedicated character development tools
- **Story Templates**: Pre-built story structures for different ages
- **Collaborative Planning**: Multiple children can plan together
- **Story Variations**: Generate multiple story versions from same planning

### Integration Opportunities
- **Educational Platforms**: Integration with learning management systems
- **Parent Apps**: Mobile apps for story creation with children
- **Classroom Tools**: Teacher-friendly interfaces for group storytelling
- **Accessibility**: Voice input and output for children with disabilities 