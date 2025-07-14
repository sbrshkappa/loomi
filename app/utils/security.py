"""
Security utility functions for the application.
This module contains security-related helper functions.
"""

import hashlib
import secrets
import string
from typing import Optional
import os

def generate_secure_token(length: int = 32) -> str:
    """
    Generate a secure random token.
    
    Args:
        length: Length of the token
        
    Returns:
        Secure random token
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password
        hashed: Hashed password
        
    Returns:
        True if password matches hash
    """
    return hash_password(password) == hashed

def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        input_string: Raw input string
        
    Returns:
        Sanitized string
    """
    import html
    return html.escape(input_string.strip())

def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format
    """
    if not api_key:
        return False
    
    # Basic validation - can be enhanced based on specific requirements
    return len(api_key) >= 10 and api_key.isalnum()

def get_environment_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Safely get environment variable.
    
    Args:
        key: Environment variable key
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default) 