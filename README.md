# AI Storyteller Agent

A modern, production-ready AI application for generating children's stories and illustrated storybooks. This application provides both a chat interface and REST API for story generation with automatic illustration and PDF creation.

## Features

- 🤖 **AI-Powered Story Generation**: Generate engaging children's stories using advanced language models
- 🎨 **Automatic Illustration**: Create storybook illustrations using AI image generation
- 📚 **PDF Storybook Creation**: Automatically generate PDF storybooks with text and images
- 💬 **Interactive Chat Interface**: Chainlit-based chat interface for story creation
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
   python app/main.py
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

### Chat Interface

1. Start the Chainlit application:
   ```bash
   python app/main.py
   ```

2. Open your browser to the provided URL (usually `http://localhost:8000`)

3. Start chatting with the AI storyteller:
   - Ask for a story about specific characters or themes
   - Provide images for context
   - Request storybook illustrations

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
  ]
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

## Development

### Setup Development Environment

```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
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
4. **Chat Interface**: Interactive conversation with the AI storyteller
5. **REST API**: Programmatic access to all functionality

### Service Layer

- **AI Services**: OpenAI, Ideogram, and other AI provider integrations
- **Storage Services**: Database operations and file management
- **External Services**: Third-party API integrations

### Data Models

- **Database Models**: SQLAlchemy models for data persistence
- **API Models**: Pydantic models for request/response validation

## Deployment

### Docker

```bash
# Build image
docker build -t ai-storyteller .

# Run container
docker run -p 8000:8000 ai-storyteller
```

### Production Considerations

1. **Environment Variables**: Use proper secret management
2. **Database**: Use production database (PostgreSQL, MySQL)
3. **Caching**: Implement Redis for session management
4. **Monitoring**: Add logging and monitoring
5. **Security**: Implement proper authentication and authorization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/docs`

## Roadmap

- [ ] User authentication and management
- [ ] Database integration for story persistence
- [ ] Advanced image generation options
- [ ] Multi-language support
- [ ] Story templates and themes
- [ ] Collaborative story creation
- [ ] Mobile application
- [ ] Advanced analytics and insights 