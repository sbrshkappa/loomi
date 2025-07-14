"""
Unit tests for configuration module.
"""

import pytest
import os
from unittest.mock import patch

from app.config.settings import get_configuration, get_generation_kwargs
from app.config.models import ModelRegistry, ModelConfig


class TestSettings:
    """Test settings configuration."""
    
    @patch.dict(os.environ, {
        'AI_MODEL_CONFIG': 'openai_gpt-4',
        'OPENAI_API_KEY': 'test_key',
        'OPENAI_ENDPOINT': 'https://api.openai.com/v1',
        'AI_TEMPERATURE': '0.8',
        'AI_MAX_TOKENS': '4000',
        'DEBUG': 'true'
    })
    def test_get_configuration(self):
        """Test configuration retrieval."""
        config = get_configuration()
        
        assert config['model'] == 'gpt-4o-mini'
        assert config['api_key'] == 'test_key'
        assert config['endpoint_url'] == 'https://api.openai.com/v1'
        assert config['debug'] is True
    
    @patch.dict(os.environ, {
        'AI_TEMPERATURE': '0.9',
        'AI_MAX_TOKENS': '3000'
    })
    def test_get_generation_kwargs(self):
        """Test generation kwargs retrieval."""
        kwargs = get_generation_kwargs()
        
        assert kwargs['temperature'] == 0.9
        assert kwargs['max_tokens'] == 3000


class TestModelRegistry:
    """Test model registry."""
    
    def test_get_available_models(self):
        """Test getting available models."""
        models = ModelRegistry.get_available_models()
        
        assert 'openai_gpt-4' in models
        assert 'mistral_7B' in models
        assert 'mistral_7B_instruct' in models
        
        # Check model config structure
        gpt4_config = models['openai_gpt-4']
        assert isinstance(gpt4_config, ModelConfig)
        assert gpt4_config.name == 'OpenAI GPT-4'
        assert gpt4_config.supports_vision is True
    
    def test_get_model_config(self):
        """Test getting specific model config."""
        config = ModelRegistry.get_model_config('openai_gpt-4')
        assert config.name == 'OpenAI GPT-4'
        
        # Test fallback to default
        config = ModelRegistry.get_model_config('nonexistent')
        assert config.name == 'OpenAI GPT-4'
    
    def test_get_model_names(self):
        """Test getting model names."""
        names = ModelRegistry.get_model_names()
        expected_names = ['mistral_7B_instruct', 'mistral_7B', 'openai_gpt-4']
        
        assert all(name in names for name in expected_names) 