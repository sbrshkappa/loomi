"""
Utility helper functions for the application.
This module contains general-purpose helper functions.
"""

from typing import List, Dict, Any, Optional
from langsmith import traceable

@traceable
def get_latest_user_message(message_history: List[Dict[str, Any]]) -> Optional[str]:
    """
    Get the latest user message from the message history.
    
    Args:
        message_history: List of message dictionaries
        
    Returns:
        The content of the latest user message, or None if not found
    """
    # Iterate through the message history in reverse to find the last user message
    for message in reversed(message_history):
        if message['role'] == 'user':
            return message['content']
    return None

def format_character_description(character: Dict[str, Any]) -> str:
    """
    Format character description for image generation.
    
    Args:
        character: Character dictionary with name and features
        
    Returns:
        Formatted character description string
    """
    name = character.get('character_name', 'Unknown')
    features = character.get('character_features', '')
    return f"{name}: {features}"

def validate_story_data(story_data: Dict[str, Any]) -> bool:
    """
    Validate story data structure.
    
    Args:
        story_data: Story data dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['title', 'characters', 'cover_picture_description', 'num_pages', 'pages']
    
    for field in required_fields:
        if field not in story_data:
            return False
    
    if not isinstance(story_data['characters'], list):
        return False
    
    if not isinstance(story_data['pages'], list):
        return False
    
    return True

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    return sanitized 