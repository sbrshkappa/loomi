# Contributing to Loomi App

Thank you for your interest in contributing to the Loomi App! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- OpenAI API key (or alternative AI provider)
- Ideogram API key (for image generation)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/loomi-app.git
   cd loomi-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Use descriptive test names
- Test both success and error cases

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Update documentation if needed
5. Run tests and ensure they pass
6. Submit a pull request with a clear description

## Project Structure

### Key Directories

- `app/`: Main application code
- `tests/`: Test files
- `docs/`: Documentation
- `scripts/`: Utility scripts
- `templates/`: HTML templates
- `static/`: Static assets

### Architecture

The application follows a modular architecture:

- **API Layer**: FastAPI routes and middleware
- **Core Logic**: Business logic and AI agents
- **Services**: External service integrations
- **Models**: Data models and schemas
- **Utils**: Helper functions and utilities

## Adding New Features

### Audio Features

When adding new audio features:

1. Update `app/services/ai/audio_generator.py`
2. Add tests in `tests/test_audio_generator.py`
3. Update API endpoints if needed
4. Document the new feature

### Story Generation

When modifying story generation:

1. Update prompts in `app/core/prompts/`
2. Test with different story types
3. Ensure age-appropriate content
4. Update documentation

### Image Generation

When adding new image features:

1. Update `app/services/ai/storybook_generator.py`
2. Test with different image styles
3. Ensure proper error handling
4. Update API documentation

## Reporting Issues

When reporting issues:

1. Use the issue template
2. Provide clear steps to reproduce
3. Include error messages and logs
4. Specify your environment (OS, Python version, etc.)

## Getting Help

- Check the documentation in `docs/`
- Look at existing issues and PRs
- Ask questions in discussions
- Join our community chat

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to Loomi App! 🚀 