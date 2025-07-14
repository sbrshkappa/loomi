"""
Database models for the application.
This module contains SQLAlchemy models for data persistence.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication and user management."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Story(Base):
    """Story model for storing generated stories."""
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=True)  # Optional user association
    session_id = Column(String(100), index=True)
    age_group = Column(String(20))  # e.g., "3-7", "7-12"
    characters = Column(JSON)  # Store character descriptions as JSON
    settings = Column(JSON)  # Store story settings as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Storybook(Base):
    """Storybook model for storing generated storybooks."""
    __tablename__ = "storybooks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    story_id = Column(Integer, nullable=True)  # Optional story association
    user_id = Column(Integer, nullable=True)  # Optional user association
    session_id = Column(String(100), index=True)
    pdf_filename = Column(String(255), nullable=False)
    cover_image_url = Column(String(500))
    num_pages = Column(Integer, default=0)
    characters = Column(JSON)  # Store character descriptions as JSON
    cover_description = Column(Text)
    pages = Column(JSON)  # Store page data as JSON
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

class ChatSession(Base):
    """Chat session model for storing conversation history."""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=True)  # Optional user association
    message_history = Column(JSON)  # Store message history as JSON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ImageGeneration(Base):
    """Image generation model for tracking generated images."""
    __tablename__ = "image_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    storybook_id = Column(Integer, nullable=True)
    page_number = Column(Integer, default=0)  # 0 for cover
    image_url = Column(String(500))
    local_filename = Column(String(255))
    prompt = Column(Text)
    model_used = Column(String(50))  # e.g., "dall-e-3", "ideogram"
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True)) 