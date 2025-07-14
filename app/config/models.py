"""
AI model configurations and settings.
This module defines the available AI models and their configurations.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    name: str
    endpoint_url: str
    api_key: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 5000
    supports_vision: bool = False
    supports_streaming: bool = True

class ModelRegistry:
    """Registry for available AI models."""
    
    @staticmethod
    def get_available_models() -> Dict[str, ModelConfig]:
        """Get all available model configurations."""
        return {
            "mistral_7B_instruct": ModelConfig(
                name="Mistral 7B Instruct",
                endpoint_url="MISTRAL_7B_INSTRUCT_ENDPOINT",
                api_key="RUNPOD_API_KEY",
                model="mistralai/Mistral-7B-Instruct-v0.2",
                supports_vision=False
            ),
            "mistral_7B": ModelConfig(
                name="Mistral 7B",
                endpoint_url="MISTRAL_7B_ENDPOINT", 
                api_key="RUNPOD_API_KEY",
                model="mistralai/Mistral-7B-v0.1",
                supports_vision=False
            ),
            "openai_gpt-4": ModelConfig(
                name="OpenAI GPT-4",
                endpoint_url="OPENAI_ENDPOINT",
                api_key="OPENAI_API_KEY", 
                model="gpt-4o-mini",
                supports_vision=True
            )
        }
    
    @staticmethod
    def get_model_config(model_key: str) -> ModelConfig:
        """Get configuration for a specific model."""
        models = ModelRegistry.get_available_models()
        return models.get(model_key, models["openai_gpt-4"])
    
    @staticmethod
    def get_model_names() -> List[str]:
        """Get list of available model names."""
        return list(ModelRegistry.get_available_models().keys()) 