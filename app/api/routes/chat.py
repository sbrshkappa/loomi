"""
Chat API routes.
This module contains the chat-related API endpoints.
"""

import os
import json
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from types import SimpleNamespace

from app.api.models.chat import ChatRequest, ChatResponse, StorybookRequest, StorybookResponse, ErrorResponse
from app.config.settings import get_configuration, get_generation_kwargs
from app.services.ai.storybook_generator import get_storybook_illustration
from app.utils.helpers import validate_story_data
from app.utils.security import generate_secure_token
import openai

router = APIRouter(prefix="/api/v1", tags=["chat"])

# Store message history in memory (consider using a proper database in production)
message_histories: Dict[str, List[Dict]] = {}

# Get configuration
config = get_configuration()
gen_kwargs = get_generation_kwargs()

# Initialize the OpenAI async client
client = openai.AsyncClient(
    api_key=config["api_key"], 
    base_url=config["endpoint_url"]
)

async def generate_response(client, message_history, gen_kwargs):
    """Generate AI response."""
    response = await client.chat.completions.create(
        messages=message_history,
        stream=False,
        **gen_kwargs
    )
    return response.choices[0].message.content

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for story generation.
    
    Args:
        request: Chat request containing messages and optional image
        
    Returns:
        Chat response with AI-generated content
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or generate_secure_token(16)
        
        # Initialize or get message history
        if session_id not in message_histories:
            from app.core.prompts.prompt_factory import get_pdf_prompt
            message_histories[session_id] = [
                {"role": "system", "content": get_pdf_prompt()}
            ]
        
        # Add user message to history
        message_histories[session_id].append(request.messages[-1].dict())
        
        # Generate response
        response_content = await generate_response(client, message_histories[session_id], gen_kwargs)
        
        # Check if response contains storybook generation request
        if "get_storybook_illustration" in response_content:
            try:
                # Parse the storybook generation request
                story_data = json.loads(response_content, object_hook=lambda d: SimpleNamespace(**d))
                
                # Generate the storybook
                story_book_name = await get_storybook_illustration(
                    story_data.arguments.title,
                    story_data.arguments.characters,
                    story_data.arguments.cover_picture_description,
                    story_data.arguments.num_pages,
                    story_data.arguments.pages
                )
                
                return ChatResponse(
                    response=response_content,
                    storybook_name=story_book_name,
                    session_id=session_id
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Add assistant response to history
        message_histories[session_id].append({"role": "assistant", "content": response_content})
        
        return ChatResponse(
            response=response_content,
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio-chat", response_model=ChatResponse)
async def audio_chat(request: ChatRequest):
    """
    Audio-optimized chat endpoint for story generation.
    
    Args:
        request: Chat request containing messages and optional image
        
    Returns:
        Chat response with AI-generated content optimized for audio
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or generate_secure_token(16)
        
        # Initialize or get message history with audio-specific prompts
        if session_id not in message_histories:
            from app.core.prompts.prompt_factory import get_audio_storybook_prompt
            message_histories[session_id] = [
                {"role": "system", "content": get_audio_storybook_prompt()}
            ]
        
        # Add user message to history
        message_histories[session_id].append(request.messages[-1].dict())
        
        # Generate response
        response_content = await generate_response(client, message_histories[session_id], gen_kwargs)
        
        # Check if response contains storybook generation request
        if "get_storybook_illustration" in response_content:
            try:
                # Parse the storybook generation request
                story_data = json.loads(response_content, object_hook=lambda d: SimpleNamespace(**d))
                
                # Generate the storybook
                story_book_name = await get_storybook_illustration(
                    story_data.arguments.title,
                    story_data.arguments.characters,
                    story_data.arguments.cover_picture_description,
                    story_data.arguments.num_pages,
                    story_data.arguments.pages
                )
                
                return ChatResponse(
                    response=response_content,
                    storybook_name=story_book_name,
                    session_id=session_id
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Add assistant response to history
        message_histories[session_id].append({"role": "assistant", "content": response_content})
        
        return ChatResponse(
            response=response_content,
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/storybook", response_model=StorybookResponse)
async def generate_storybook(request: StorybookRequest):
    """
    Direct storybook generation endpoint.
    
    Args:
        request: Storybook generation request
        
    Returns:
        Storybook response with generated PDF or audio info
    """
    try:
        # Validate story data
        if not validate_story_data(request.dict()):
            raise HTTPException(status_code=400, detail="Invalid story data format")

        if request.output_type == "pdf":
            # Generate storybook PDF
            story_book_name = await get_storybook_illustration(
                request.title,
                request.characters,
                request.cover_picture_description,
                request.num_pages,
                request.pages
            )
            return StorybookResponse(
                storybook_name=story_book_name,
                download_url=f"/api/v1/storybook/{story_book_name}",
                status="success"
            )
        elif request.output_type == "audio":
            from app.services.ai.audio_generator import generate_audio_from_text
            from app.core.prompts.audio_prompts import AUDIO_STORY_PROMPT, AUDIO_STORYBOOK_PROMPT
            import uuid
            import os

            # For audio output, we want to enhance the story text with audio-specific details
            # Combine all story pages into a single string with enhanced audio narration
            enhanced_story_text = ""
            
            # Add a warm introduction for audio
            enhanced_story_text += f"Welcome to the story of {request.title}. "
            
            # Process each page with audio enhancements
            for i, page in enumerate(request.pages):
                page_text = page["page_text"]
                
                # Add page transition for audio
                if i > 0:
                    enhanced_story_text += " "
                
                # Enhance the page text for audio narration
                enhanced_story_text += page_text
            
            # Add a warm closing for audio
            enhanced_story_text += " The end. Sweet dreams, little one."
            
            audio_file_name = f"storybook_{uuid.uuid4().hex}.mp3"
            audio_output_path = os.path.join("audio_outputs", audio_file_name)  # Make sure this dir exists

            # Generate audio with enhanced text and auto-detected voice style
            generate_audio_from_text(enhanced_story_text, audio_output_path, language="en", voice_style=None)

            audio_url = f"/api/v1/audio/{audio_file_name}"
            return StorybookResponse(
                storybook_name=request.title,
                audio_url=audio_url,
                status="success"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid output_type. Must be 'pdf' or 'audio'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/story", response_model=ChatResponse)
async def generate_story(request: ChatRequest, output_type: str = Query("pdf", description="Type of output desired")):
    """
    Flexible story generation endpoint with configurable output type.
    
    Args:
        request: Chat request containing messages and optional image
        output_type: Type of output desired (text, pdf, audio, audio_pdf, audio_storybook)
        
    Returns:
        Chat response with AI-generated content
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or generate_secure_token(16)
        
        # Get the appropriate prompt based on output type
        from app.core.prompts.prompt_factory import PromptFactory, AVAILABLE_OUTPUT_TYPES
        
        if output_type not in AVAILABLE_OUTPUT_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid output_type: {output_type}. Available types: {list(AVAILABLE_OUTPUT_TYPES.keys())}"
            )
        
        # Initialize or get message history with the appropriate prompt
        if session_id not in message_histories:
            prompt = PromptFactory.get_prompt(output_type)
            message_histories[session_id] = [
                {"role": "system", "content": prompt}
            ]
        
        # Add user message to history
        message_histories[session_id].append(request.messages[-1].dict())
        
        # Generate response
        response_content = await generate_response(client, message_histories[session_id], gen_kwargs)
        
        # Handle audio generation for audio output types
        print(f"DEBUG: output_type = {output_type}")  # Debug line
        if output_type in ["audio", "audio_pdf", "audio_storybook"]:
            try:
                # Import audio generation function
                from app.services.ai.audio_generator import generate_audio_from_text
                import uuid
                import os
                
                # Create audio outputs directory if it doesn't exist
                os.makedirs("audio_outputs", exist_ok=True)
                
                # Generate audio file name
                audio_file_name = f"story_{uuid.uuid4().hex}.mp3"
                audio_output_path = os.path.join("audio_outputs", audio_file_name)
                
                # Generate audio from the story text with auto-detected voice style
                generate_audio_from_text(response_content, audio_output_path, language="en", voice_style=None)
                
                # Add assistant response to history
                message_histories[session_id].append({"role": "assistant", "content": response_content})
                
                # Create audio URL
                audio_url = f"/api/v1/audio/{audio_file_name}"
                
                return ChatResponse(
                    response=response_content,
                    storybook_name=None,
                    audio_url=audio_url,
                    session_id=session_id,
                    output_type=output_type
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")
        
        # Check if response contains storybook generation request (for PDF types)
        if "get_storybook_illustration" in response_content and output_type in ["pdf", "audio_pdf", "audio_storybook"]:
            try:
                # Parse the storybook generation request
                story_data = json.loads(response_content, object_hook=lambda d: SimpleNamespace(**d))
                
                # Generate the storybook
                story_book_name = await get_storybook_illustration(
                    story_data.arguments.title,
                    story_data.arguments.characters,
                    story_data.arguments.cover_picture_description,
                    story_data.arguments.num_pages,
                    story_data.arguments.pages
                )
                
                return ChatResponse(
                    response=response_content,
                    storybook_name=story_book_name,
                    session_id=session_id,
                    output_type=output_type
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Add assistant response to history
        message_histories[session_id].append({"role": "assistant", "content": response_content})
        
        return ChatResponse(
            response=response_content,
            session_id=session_id,
            output_type=output_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/storybook/{storybook_name}")
async def get_storybook(storybook_name: str):
    """
    Download storybook PDF.
    
    Args:
        storybook_name: Name of the storybook file
        
    Returns:
        PDF file response
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_file_path = os.path.join(current_dir, '..', '..', '..', storybook_name)
        
        if not os.path.exists(pdf_file_path):
            raise HTTPException(status_code=404, detail="Storybook not found")
        
        return FileResponse(
            pdf_file_path,
            media_type="application/pdf",
            filename=storybook_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/history")
async def get_chat_history(session_id: str):
    """
    Get chat history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Chat history for the session
    """
    if session_id not in message_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"session_id": session_id, "history": message_histories[session_id]}

@router.post("/plan-story", response_model=ChatResponse)
async def plan_story(request: ChatRequest):
    """
    Interactive story planning endpoint for collaborative story creation.
    
    This endpoint uses a conversational approach to help children and parents
    plan and develop story ideas together before generating the final story.
    
    Args:
        request: Chat request containing messages for story planning
        
    Returns:
        Chat response with planning conversation
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or generate_secure_token(16)
        
        # Initialize or get message history with story planning prompt
        if session_id not in message_histories:
            from app.core.prompts.base_prompts import STORY_PLANNING_PROMPT
            message_histories[session_id] = [
                {"role": "system", "content": STORY_PLANNING_PROMPT}
            ]
        
        # Add user message to history
        message_histories[session_id].append(request.messages[-1].dict())
        
        # Generate response
        response_content = await generate_response(client, message_histories[session_id], gen_kwargs)
        
        # Add assistant response to history
        message_histories[session_id].append({"role": "assistant", "content": response_content})
        
        return ChatResponse(
            response=response_content,
            session_id=session_id,
            output_type="planning"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-story", response_model=ChatResponse)
async def generate_final_story(session_id: str, output_type: str = Query("audio", description="Type of output desired")):
    """
    Generate the final story from a planning session.
    
    This endpoint takes the planning conversation and generates the final story
    in the requested format (audio, pdf, etc.).
    
    Args:
        session_id: Session identifier from the planning phase
        output_type: Type of output desired (text, pdf, audio, audio_pdf, audio_storybook)
        
    Returns:
        Chat response with generated story and optional audio/PDF
    """
    try:
        # Check if session exists
        if session_id not in message_histories:
            raise HTTPException(status_code=404, detail="Planning session not found. Please start with /plan-story first.")
        
        # Get the appropriate prompt based on output type
        from app.core.prompts.prompt_factory import PromptFactory, AVAILABLE_OUTPUT_TYPES
        
        if output_type not in AVAILABLE_OUTPUT_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid output_type: {output_type}. Available types: {list(AVAILABLE_OUTPUT_TYPES.keys())}"
            )
        
        # Create a new message history for story generation
        # Include the planning conversation as context
        planning_conversation = message_histories[session_id].copy()
        
        # Add the story generation prompt
        story_prompt = PromptFactory.get_prompt(output_type)
        story_generation_messages = [
            {"role": "system", "content": story_prompt},
            {"role": "user", "content": "Based on our planning conversation, please generate the final story. Here's what we planned:"}
        ]
        
        # Add key points from the planning conversation
        planning_summary = "Planning Summary:\n"
        for msg in planning_conversation:
            if msg["role"] == "user":
                planning_summary += f"- User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                planning_summary += f"- Assistant: {msg['content']}\n"
        
        story_generation_messages.append({"role": "user", "content": planning_summary})
        
        # Generate the final story
        response_content = await generate_response(client, story_generation_messages, gen_kwargs)
        
        # Handle audio generation for audio output types
        if output_type in ["audio", "audio_pdf", "audio_storybook"]:
            try:
                # Import audio generation function
                from app.services.ai.audio_generator import generate_audio_from_text
                import uuid
                import os
                
                # Create audio outputs directory if it doesn't exist
                os.makedirs("audio_outputs", exist_ok=True)
                
                # Generate audio file name
                audio_file_name = f"story_{uuid.uuid4().hex}.mp3"
                audio_output_path = os.path.join("audio_outputs", audio_file_name)
                
                # Generate audio from the story text
                generate_audio_from_text(response_content, audio_output_path, language="en")
                
                # Create audio URL
                audio_url = f"/api/v1/audio/{audio_file_name}"
                
                return ChatResponse(
                    response=response_content,
                    storybook_name=None,
                    audio_url=audio_url,
                    session_id=session_id,
                    output_type=output_type
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")
        
        # Check if response contains storybook generation request (for PDF types)
        if "get_storybook_illustration" in response_content and output_type in ["pdf", "audio_pdf", "audio_storybook"]:
            try:
                # Parse the storybook generation request
                story_data = json.loads(response_content, object_hook=lambda d: SimpleNamespace(**d))
                
                # Generate the storybook
                story_book_name = await get_storybook_illustration(
                    story_data.arguments.title,
                    story_data.arguments.characters,
                    story_data.arguments.cover_picture_description,
                    story_data.arguments.num_pages,
                    story_data.arguments.pages
                )
                
                return ChatResponse(
                    response=response_content,
                    storybook_name=story_book_name,
                    session_id=session_id,
                    output_type=output_type
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        return ChatResponse(
            response=response_content,
            session_id=session_id,
            output_type=output_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a chat session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Success message
    """
    if session_id in message_histories:
        del message_histories[session_id]
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found") 

@router.get("/audio/{audio_file_name}")
async def get_audio(audio_file_name: str):
    """
    Get audio file.
    
    Args:
        audio_file_name: Name of the audio file
        
    Returns:
        Audio file response
    """
    import os
    audio_path = os.path.join("audio_outputs",audio_file_name)
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/mpeg", filename=audio_file_name)