"""
API models for chat functionality.
This module contains Pydantic models for request/response handling.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from enum import Enum

class OutputType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    AUDIO = "audio"
    AUDIO_PDF = "audio_pdf"
    AUDIO_STORYBOOK = "audio_storybook"

class Message(BaseModel):
    """Message model for chat conversations."""
    role: str
    content: Union[str, List[Dict[str, Any]]]

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    messages: List[Message]
    image_base64: Optional[str] = None
    session_id: Optional[str] = None
    output_type: OutputType = OutputType.PDF

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    storybook_name: Optional[str] = None
    audio_url: Optional[str] = None
    session_id: Optional[str] = None
    output_type: Optional[str] = None

class StorybookRequest(BaseModel):
    """Request model for storybook generation."""
    title: str
    characters: List[Dict[str, str]]
    cover_picture_description: str
    num_pages: int
    pages: List[Dict[str, Any]]
    output_type: OutputType = OutputType.PDF

class StorybookResponse(BaseModel):
    """Response model for storybook generation."""
    storybook_name: str
    download_url: Optional[str] = None
    audio_url: Optional[str] = None  # URL for audio file if output_type is audio
    status: str = "success"

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    status_code: int = 400 