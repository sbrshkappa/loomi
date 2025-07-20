# AI Storyteller Agent

A modern, production-ready AI application for generating children's stories and illustrated storybooks. This application provides both a chat interface and REST API for story generation with automatic illustration, PDF creation, and expressive audio narration.

## Features

- 🤖 **AI-Powered Story Generation**: Generate engaging children's stories using advanced language models
- 🎨 **Automatic Illustration**: Create storybook illustrations using AI image generation
- 📚 **PDF Storybook Creation**: Automatically generate PDF storybooks with text and images
- 🔊 **Expressive Audio Narration**: Generate dynamic, emotional audio narration (MP3) using OpenVoice V2 + MeloTTS
- 💬 **Interactive Chat Interface**: Chainlit-based chat interface for story creation and narration
- 🔌 **REST API**: Full REST API for integration with other applications
- 🎯 **Age-Appropriate Content**: Tailored story length and content for different age groups
- 🔧 **Modular Architecture**: Clean, maintainable codebase following best practices

## Project Structure

```
app/
├── config/            # Configuration management
│   ├── settings.py    # Environment-specific settings
│   └── models.py      # AI model configurations
├── core/              # Core business logic
│   ├── agents/        # AI agent implementations
│   ├── prompts/       # Prompt templates and management
│   ├── tools/         # Agent tools and utilities
│   └── memory/        # Conversation and context memory
├── api/               # API layer
│   ├── routes/        # API endpoints
│   ├── middleware/    # Authentication, CORS, etc.
│   ├── models/        # Pydantic models
│   └── app.py         # FastAPI application
├── services/          # External service integrations
│   ├── ai/           # AI service clients
│   ├── storage/      # Database operations
│   └── external/     # Third-party APIs
├── models/           # Data models and schemas
│   ├── database.py   # Database models
│   └── api.py        # API request/response models
├── utils/            # Utility functions
│   ├── security.py   # Security utilities
│   └── helpers.py    # General helpers
└── main.py           # Application entry point
```

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (or alternative AI provider)
- Ideogram API key (for image generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd loomi-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the application**

   **Chat Interface (Chainlit):**
   ```bash
   chainlit run app/main.py
   ```

   **REST API:**
   ```bash
   python app/api/app.py
   ```

## Configuration

### Environment Variables

Copy `env.example` to `.env` and configure the following variables:

```bash
# AI Model Configuration
AI_MODEL_CONFIG=openai_gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=5000

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_ENDPOINT=https://api.openai.com/v1

# Ideogram Configuration (Alternative image generation)
IDEOGRAM_API_KEY=your_ideogram_api_key_here
IDEOGRAM_ENDPOINT=https://api.ideogram.ai/api/v1

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### AI Model Options

The application supports multiple AI models:

- **OpenAI GPT-4**: Default model with vision capabilities
- **Mistral 7B**: Open-source alternative via RunPod
- **Mistral 7B Instruct**: Instruction-tuned version

Set `AI_MODEL_CONFIG` in your environment to switch between models.

## Usage

### Chat Interface (Chainlit)

1. Start the Chainlit application:
   ```bash
   chainlit run app/main.py
   ```

2. Open your browser to the provided URL (usually `http://localhost:8000`)

3. Start chatting with the AI storyteller:
   - Ask for a story about specific characters or themes
   - Provide images for context
   - Request storybook illustrations
   - **Request audio narration**: Say things like "I would like to listen to this story" or "Can you narrate this for me?" to receive expressive audio narration (MP3) of your story.

### REST API

The API provides endpoints for programmatic access:

#### Chat Endpoint
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Tell me a story about a brave little mouse"
    }
  ],
  "session_id": "optional-session-id"
}
```

#### Storybook Generation
```bash
POST /api/v1/storybook
Content-Type: application/json

{
  "title": "The Brave Little Mouse",
  "characters": [
    {
      "character_name": "Mickey",
      "character_features": "A small brown mouse with big ears"
    }
  ],
  "cover_picture_description": "A brave little mouse standing on a cheese",
  "num_pages": 3,
  "pages": [
    {
      "page_num": 1,
      "page_text": "Once upon a time...",
      "page_picture_description": "A cozy mouse hole"
    }
  ],
  "output_type": "audio"  # Use "audio", "pdf", or "audio_pdf"
}
```

#### Flexible Story Generation (Text, Audio, PDF)
```bash
POST /api/v1/story
Content-Type: application/json

{
  "messages": [
    { "role": "user", "content": "Tell me a story about a magical forest" }
  ],
  "output_type": "audio"  # or "pdf", "audio_pdf", "text"
}
```

#### Download Storybook
```bash
GET /api/v1/storybook/{storybook_name}
```

### API Documentation

When running the API server, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Audio Narration

Loomi can generate expressive audio narration for any story, using OpenVoice V2 and MeloTTS for dynamic, emotional storytelling.

### Audio Features
- 🎤 **Expressive Narration**: Audio adapts to the story's emotions, with changes in tone, rhythm, and character voices
- 🗣️ **Dynamic Voice Styles**: Per-segment voice style switching for laughter, excitement, gentle moments, and more
- 🔄 **Flexible Output**: Generate audio-only, audio+PDF, or classic text storybooks
- 📥 **Downloadable MP3**: Receive high-quality MP3 narration via API or Chainlit

### How to Request Audio
- **In Chainlit**: After generating a story, say "I would like to listen to this story" or "Can you narrate this for me?"
- **Via API**: Set `output_type` to `audio` or `audio_pdf` in your request

### Example: Requesting Audio in Chainlit
```
User: Tell me a story about a dragon and a princess
AI: [Story is generated]
User: Can you narrate this for me?
AI: [Sends MP3 audio narration file]
```

### Example: Requesting Audio via API
```
POST /api/v1/story
{
  "messages": [
    { "role": "user", "content": "Tell me a story about a dragon and a princess" }
  ],
  "output_type": "audio"
}
```

## RAG Enhancement (Retrieval-Augmented Generation)

Loomi includes optional RAG enhancement that improves story quality by incorporating relevant Aesop's Fables and classic stories.

### Features
- **🎯 Smart Retrieval**: Finds relevant classic fables based on user requests
- **📚 Educational Enhancement**: Adds moral lessons and educational content
- **🔄 Toggle Control**: Easy enable/disable with environment variable
- **📊 Research Metrics**: Track RAG vs non-RAG performance
- **🎭 Context Detection**: Automatically detects story requests

### Enable RAG Enhancement

**Environment Variable:**
```bash
export ENABLE_RAG=true
python -m chainlit run app/main.py
```

**Direct Code Change:**
```python
# In app/main.py, change:
ENABLE_RAG = True  # Instead of False
```

### How It Works

When RAG is enabled, the system:
1. **Detects story requests** using keywords and context
2. **Retrieves relevant fables** from a vector database of 129 Aesop's Fables
3. **Enhances system prompts** with classic themes and moral lessons
4. **Tracks performance metrics** for research and comparison

### Example Enhancement

**Original Prompt:**
```
Story Generation:
When you have all the information needed, write a complete, engaging story...
```

**With RAG Enhancement:**
```
Story Generation:

**RAG Enhancement - Relevant Aesop's Fables for Inspiration:**
THE LION AND THE MOUSE: A mighty lion spares a tiny mouse's life...
**Consider these themes from classic fables:** kindness, friendship
**Consider these character types:** lion, mouse
**Use these classic fables as inspiration to create a new, original story...**

When you have all the information needed, write a complete, engaging story...
```

### Testing RAG

```bash
# Test RAG toggle functionality
python tests/integration/test_rag_toggle.py

# Run comprehensive RAG tests
python scripts/test_rag_integration.py
```

### Expected Improvements
- **Educational Value**: +15-25% improvement
- **Moral Lesson Presence**: +30-40% improvement
- **Character Development**: Better character arcs
- **Performance Overhead**: +2-3 seconds

## Flexible Prompt System

Loomi uses a modular, composable prompt architecture:
- **Base Prompts**: For classic story structure
- **Audio Prompts**: For expressive, narration-optimized stories
- **Image Prompts**: For vivid illustration descriptions
- **Prompt Factory**: Combine prompts for any output type (text, audio, image, or all)

## Testing & Continuous Integration

- All tests are in the `tests/` folder (unit, integration, and fixtures)
- Run tests with:
  ```bash
  pytest tests/
  ```
- Lint, format, and type-check with:
  ```bash
  flake8 app/ tests/
  black app/ tests/
  mypy app/
  ```
- GitHub Actions CI runs tests, lint, and security checks on every push/PR

## Development

### Setup Development Environment

```bash
pip install -r requirements-dev.txt
```

### Project Structure Guidelines

- **Configuration**: All configuration should be in `app/config/`
- **Business Logic**: Core functionality goes in `app/core/`
- **API Layer**: API-related code in `app/api/`
- **Services**: External integrations in `app/services/`
- **Models**: Data models in `app/models/`
- **Utilities**: Helper functions in `app/utils/`

## Architecture

### Core Components

1. **Story Generator**: AI-powered story creation with age-appropriate content
2. **Image Generator**: AI image generation for storybook illustrations
3. **PDF Generator**: Automatic PDF creation with text and images
4. **Audio Generator**: Expressive, dynamic audio narration (MP3)
5. **Chat Interface**: Interactive conversation with the AI storyteller
6. **REST API**: Programmatic access to all functionality

### Service Layer

- **AI Services**: OpenAI, Ideogram, and other AI provider integrations
- **Storage Services**: Database operations and file management
- **External Services**: Third-party API integrations

### Data Models

- **Database Models**: SQLAlchemy models for data persistence
- **API Models**: Pydantic models for request/response validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] User authentication and management
- [ ] Database integration for story persistence
- [ ] Advanced image generation options
- [ ] Multi-language support
- [ ] Story templates and themes
- [ ] Collaborative story creation
- [ ] Mobile application
- [ ] Advanced analytics and insights 