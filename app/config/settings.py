"""
Application settings and configuration management.
This module handles environment-specific settings and configuration.
"""

import os
from typing import Dict, Any

def get_configuration() -> Dict[str, Any]:
    """
    Get the current configuration based on environment variables.
    
    Returns:
        Dict containing the configuration settings
    """
    configurations = {
        "mistral_7B_instruct": {
            "endpoint_url": os.getenv("MISTRAL_7B_INSTRUCT_ENDPOINT"),
            "api_key": os.getenv("RUNPOD_API_KEY"),
            "model": "mistralai/Mistral-7B-Instruct-v0.2"
        },
        "mistral_7B": {
            "endpoint_url": os.getenv("MISTRAL_7B_ENDPOINT"),
            "api_key": os.getenv("RUNPOD_API_KEY"),
            "model": "mistralai/Mistral-7B-v0.1"
        },
        "openai_gpt-4": {
            "endpoint_url": os.getenv("OPENAI_ENDPOINT"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-4o-mini"
        }
    }

    # Choose configuration - can be made configurable via environment variable
    config_key = os.getenv("AI_MODEL_CONFIG", "openai_gpt-4")
    
    # Get selected configuration
    config = configurations.get(config_key, configurations["openai_gpt-4"])
    
    # Add debug flag
    config["debug"] = os.getenv("DEBUG", "false").lower() == "true"
    
    return config

def get_generation_kwargs() -> Dict[str, Any]:
    """
    Get the generation parameters for AI models.
    
    Returns:
        Dict containing generation parameters
    """
    return {
        "model": get_configuration()["model"],
        "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("AI_MAX_TOKENS", "5000"))
    } 