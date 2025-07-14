"""
Unit tests for utility functions.
"""

import pytest
from app.utils.helpers import get_latest_user_message, format_character_description, validate_story_data, sanitize_filename
from app.utils.security import generate_secure_token, hash_password, verify_password, sanitize_input, validate_api_key


class TestHelpers:
    """Test helper functions."""
    
    def test_get_latest_user_message(self):
        """Test getting latest user message."""
        message_history = [
            {"role": "system", "content": "You are a storyteller"},
            {"role": "user", "content": "Tell me a story"},
            {"role": "assistant", "content": "Once upon a time..."},
            {"role": "user", "content": "Make it about a cat"}
        ]
        
        latest = get_latest_user_message(message_history)
        assert latest == "Make it about a cat"
    
    def test_get_latest_user_message_no_user(self):
        """Test getting latest user message when none exists."""
        message_history = [
            {"role": "system", "content": "You are a storyteller"},
            {"role": "assistant", "content": "Once upon a time..."}
        ]
        
        latest = get_latest_user_message(message_history)
        assert latest is None
    
    def test_format_character_description(self):
        """Test character description formatting."""
        character = {
            "character_name": "Mickey",
            "character_features": "A small brown mouse with big ears"
        }
        
        formatted = format_character_description(character)
        assert formatted == "Mickey: A small brown mouse with big ears"
    
    def test_validate_story_data_valid(self):
        """Test story data validation with valid data."""
        story_data = {
            "title": "Test Story",
            "characters": [{"name": "Mickey"}],
            "cover_picture_description": "A test cover",
            "num_pages": 3,
            "pages": [{"page_num": 1, "content": "Test"}]
        }
        
        assert validate_story_data(story_data) is True
    
    def test_validate_story_data_invalid(self):
        """Test story data validation with invalid data."""
        # Missing required fields
        story_data = {
            "title": "Test Story"
        }
        
        assert validate_story_data(story_data) is False
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test with invalid characters
        filename = "test<>:\"/\\|?*.txt"
        sanitized = sanitize_filename(filename)
        assert sanitized == "test_______.txt"
        
        # Test with leading/trailing spaces and dots
        filename = " .test. "
        sanitized = sanitize_filename(filename)
        assert sanitized == "test"
        
        # Test with long filename
        long_filename = "a" * 300
        sanitized = sanitize_filename(long_filename)
        assert len(sanitized) == 255


class TestSecurity:
    """Test security functions."""
    
    def test_generate_secure_token(self):
        """Test secure token generation."""
        token = generate_secure_token(16)
        assert len(token) == 16
        assert token.isalnum()
        
        # Test different lengths
        token2 = generate_secure_token(32)
        assert len(token2) == 32
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) == 64  # SHA-256 hash length
        assert hashed.isalnum()
    
    def test_verify_password(self):
        """Test password verification."""
        password = "test_password"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        # Test with HTML
        input_text = "<script>alert('xss')</script>"
        sanitized = sanitize_input(input_text)
        assert sanitized == "&lt;script&gt;alert('xss')&lt;/script&gt;"
        
        # Test with whitespace
        input_text = "  test  "
        sanitized = sanitize_input(input_text)
        assert sanitized == "test"
    
    def test_validate_api_key(self):
        """Test API key validation."""
        # Valid API key
        assert validate_api_key("valid_api_key_123") is True
        
        # Invalid API keys
        assert validate_api_key("") is False
        assert validate_api_key("short") is False
        assert validate_api_key("invalid key with spaces") is False 