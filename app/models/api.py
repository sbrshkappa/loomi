"""
API models for request/response handling.
This module contains Pydantic models for API data validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AgeGroup(str, Enum):
    """Age group enumeration."""
    UNDER_3 = "under_3"
    AGES_3_7 = "3_7"
    AGES_7_12 = "7_12"
    OVER_12 = "over_12"

class StoryStatus(str, Enum):
    """Story status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Character(BaseModel):
    """Character model for story characters."""
    name: str = Field(..., description="Character name")
    description: str = Field(..., description="Character description")
    personality: Optional[str] = Field(None, description="Character personality traits")
    appearance: Optional[str] = Field(None, description="Character physical appearance")

class StorySettings(BaseModel):
    """Story settings model."""
    location: Optional[str] = Field(None, description="Story location")
    time_period: Optional[str] = Field(None, description="Time period of the story")
    mood: Optional[str] = Field(None, description="Story mood/atmosphere")
    theme: Optional[str] = Field(None, description="Story theme")

class StoryCreate(BaseModel):
    """Model for creating a new story."""
    title: str = Field(..., min_length=1, max_length=200, description="Story title")
    prompt: str = Field(..., min_length=1, description="Story generation prompt")
    age_group: AgeGroup = Field(..., description="Target age group")
    characters: Optional[List[Character]] = Field(None, description="Story characters")
    settings: Optional[StorySettings] = Field(None, description="Story settings")
    include_illustrations: bool = Field(False, description="Whether to include illustrations")

class StoryResponse(BaseModel):
    """Model for story response."""
    id: int
    title: str
    content: str
    age_group: AgeGroup
    characters: Optional[List[Character]]
    settings: Optional[StorySettings]
    created_at: datetime
    
    class Config:
        from_attributes = True

class StorybookCreate(BaseModel):
    """Model for creating a new storybook."""
    story_id: Optional[int] = Field(None, description="Associated story ID")
    title: str = Field(..., min_length=1, max_length=200, description="Storybook title")
    characters: List[Dict[str, str]] = Field(..., description="Character descriptions")
    cover_description: str = Field(..., description="Cover image description")
    num_pages: int = Field(..., ge=1, le=25, description="Number of pages")
    pages: List[Dict[str, Any]] = Field(..., description="Page content and descriptions")

class StorybookResponse(BaseModel):
    """Model for storybook response."""
    id: int
    title: str
    pdf_filename: str
    num_pages: int
    status: StoryStatus
    download_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    """Model for chat messages."""
    role: str = Field(..., description="Message role (user/assistant/system)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(None, description="Message timestamp")

class ChatSessionCreate(BaseModel):
    """Model for creating a chat session."""
    user_id: Optional[int] = Field(None, description="User ID if authenticated")

class ChatSessionResponse(BaseModel):
    """Model for chat session response."""
    session_id: str
    messages: List[ChatMessage]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(400, description="HTTP status code")

class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    version: str = Field(..., description="API version") 