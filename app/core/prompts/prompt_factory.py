"""
Prompt factory for different story generation output types.
This module provides easy access to various prompt combinations.
"""

from app.core.prompts.base_prompts import BASE_STORY_PROMPT
from app.core.prompts.image_prompts import IMAGE_GENERATION_PROMPT
from app.core.prompts.audio_prompts import AUDIO_ENHANCEMENTS, AUDIO_STORYBOOK_ENHANCEMENTS

class PromptFactory:
    """Factory for creating different prompt combinations."""
    
    @staticmethod
    def get_prompt(output_type: str = "text") -> str:
        """
        Get the appropriate prompt combination based on output type.
        
        Args:
            output_type: Type of output desired
                - "text": Basic story generation (text only)
                - "pdf": Story with images (traditional storybook)
                - "audio": Audio-optimized story (audio only)
                - "audio_pdf": Audio-optimized story with images (multimedia)
                
        Returns:
            Combined prompt string
        """
        
        if output_type == "text":
            return BASE_STORY_PROMPT
            
        elif output_type == "pdf":
            return BASE_STORY_PROMPT + IMAGE_GENERATION_PROMPT
            
        elif output_type == "audio":
            return BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS
            
        elif output_type == "audio_pdf":
            return BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + IMAGE_GENERATION_PROMPT
            
        elif output_type == "audio_storybook":
            return BASE_STORY_PROMPT + AUDIO_ENHANCEMENTS + AUDIO_STORYBOOK_ENHANCEMENTS + IMAGE_GENERATION_PROMPT
            
        else:
            raise ValueError(f"Unknown output type: {output_type}. Supported types: text, pdf, audio, audio_pdf, audio_storybook")

# Convenience functions for easy access
def get_text_prompt() -> str:
    """Get prompt for text-only story generation."""
    return PromptFactory.get_prompt("text")

def get_pdf_prompt() -> str:
    """Get prompt for PDF storybook generation (with images)."""
    return PromptFactory.get_prompt("pdf")

def get_audio_prompt() -> str:
    """Get prompt for audio-optimized story generation."""
    return PromptFactory.get_prompt("audio")

def get_audio_pdf_prompt() -> str:
    """Get prompt for audio-optimized story with images."""
    return PromptFactory.get_prompt("audio_pdf")

def get_audio_storybook_prompt() -> str:
    """Get prompt for audio storybook generation (with enhanced audio features)."""
    return PromptFactory.get_prompt("audio_storybook")

# Available output types for reference
AVAILABLE_OUTPUT_TYPES = {
    "text": "Basic story generation (text only)",
    "pdf": "Story with images (traditional storybook)",
    "audio": "Audio-optimized story (audio only)",
    "audio_pdf": "Audio-optimized story with images (multimedia)",
    "audio_storybook": "Audio storybook with enhanced features"
} 