"""
Main application entry point for the AI Storyteller Agent.
This module initializes the application and provides the main interface.
"""

import os
import asyncio
import json
import base64
import concurrent.futures
import re
from datetime import datetime
from types import SimpleNamespace

from dotenv import load_dotenv
import chainlit as cl
import openai

from app.config.settings import get_configuration
from app.core.prompts.story_prompts import SYSTEM_PROMPT, IMAGE_GENERATION_PROMPT, AUDIO_OPTIMIZED_PROMPT
from app.services.ai.storybook_generator import get_storybook_illustration
from app.utils.helpers import get_latest_user_message
from langsmith import traceable

# Load environment variables
load_dotenv()

# Get configuration
config = get_configuration()
debug = config.get("debug", False)

# Initialize the OpenAI async client
client = openai.AsyncClient(
    api_key=config["api_key"], 
    base_url=config["endpoint_url"]
)

gen_kwargs = {
    "model": config["model"],
    "temperature": 0.7,
    "max_tokens": 5000
}

# Configuration setting to enable or disable the system prompt
ENABLE_SYSTEM_PROMPT = True

@traceable
@cl.on_chat_start
def on_chat_start():    
    """Initialize chat session with system prompt."""
    message_history = [{"role": "system", "content": AUDIO_OPTIMIZED_PROMPT + IMAGE_GENERATION_PROMPT}]
    cl.user_session.set("message_history", message_history)

async def generate_response(client, message_history, gen_kwargs):
    """Generate AI response with streaming support."""
    response_message = cl.Message(content="")

    stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
    first_token = None
    should_stream_to_ui = True

    async for part in stream:
        token = part.choices[0].delta.content or ""
        if first_token is None and token.strip():
            first_token = token.strip()
            if debug:
                print(f"First non-empty token is: {first_token}")
            if first_token.startswith("{"): # This is to prevent the function call from being printed to the user on chainlit
                should_stream_to_ui = False  # Do not stream to UI if the first token starts with "{"

        if should_stream_to_ui:
            await response_message.stream_token(token)
        else:
            response_message.content += token  # Build up the response content

    if should_stream_to_ui:
        await response_message.send()

    return response_message

def extract_story_from_messages(message_history):
    """Extract story content from message history for audio generation."""
    story_content = ""
    
    # Look for the most recent assistant message that contains a story
    for message in reversed(message_history):
        if message.get("role") == "assistant" and message.get("content"):
            content = message["content"]
            # Skip function calls and system messages
            if not content.startswith("{") and not content.startswith("You are"):
                # Check if this looks like a story (has title, characters, plot)
                if any(keyword in content.lower() for keyword in ["once upon a time", "story", "chapter", "title:", "character"]):
                    story_content = content
                    break
    
    return story_content

def should_generate_audio(user_message):
    """Check if the user is requesting audio generation."""
    audio_keywords = [
        "listen", "audio", "narrate", "read aloud", "hear", "voice", 
        "speak", "tell me", "play", "sound", "recording"
    ]
    
    message_lower = user_message.lower()
    return any(keyword in message_lower for keyword in audio_keywords)

@traceable
@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages and generate responses."""
    message_history = cl.user_session.get("message_history", [])

    # Processing images if there are any
    images = [file for file in message.elements if "image" in file.mime] if message.elements else []

    if images:
        # Read the first image and encode it to base64
        with open(images[0].path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        message_history.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message.content if message.content else "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64, {base64_image}"
                    }
                }
            ]
        })
    else:
        message_history.append({"role": "user", "content": message.content})

    if debug:
        print("Message history:")
        print(message_history)
    
    # Check if user is requesting audio for an existing story
    if should_generate_audio(message.content):
        story_content = extract_story_from_messages(message_history)
        if story_content:
            # Generate audio for the existing story
            await cl.Message(content="🎵 Generating audio narration for your story, please wait...").send()
            
            def generate_audio_for_story():
                try:
                    from app.services.ai.audio_generator import generate_audio_from_text
                    import uuid
                    
                    # Create audio outputs directory if it doesn't exist
                    os.makedirs("audio_outputs", exist_ok=True)
                    
                    # Generate audio file
                    audio_file_name = f"story_{uuid.uuid4().hex}.mp3"
                    audio_output_path = os.path.join("audio_outputs", audio_file_name)
                    
                    # Generate audio with dynamic voice styles
                    generate_audio_from_text(story_content, audio_output_path, language="en", voice_style=None)
                    
                    return audio_file_name, audio_output_path
                    
                except Exception as e:
                    error_msg = f"Error generating audio: {e}"
                    print(error_msg)
                    raise ValueError(error_msg)
            
            # Use a ThreadPoolExecutor to run the blocking function in a separate thread
            loop = asyncio.get_event_loop()
            executor = concurrent.futures.ThreadPoolExecutor()
            future = loop.run_in_executor(executor, generate_audio_for_story)
            
            # Schedule the audio sending coroutine to run once the future is done
            def handle_audio_result(future):
                try:
                    result = future.result()
                    asyncio.run_coroutine_threadsafe(send_audio_file(*result), loop)
                except Exception as e:
                    error_msg = f"Error in audio generation callback: {e}"
                    print(error_msg)
                    asyncio.run_coroutine_threadsafe(
                        cl.Message(content=f"Sorry, there was an error generating audio: {str(e)}").send(), 
                        loop
                    )
            
            future.add_done_callback(handle_audio_result)
            
            # Add a response to the message history
            message_history.append({"role": "assistant", "content": "I'm generating audio narration for your story! 🎵"})
            cl.user_session.set("message_history", message_history)
            return
    
    response_message = await generate_response(client, message_history, gen_kwargs)
    
    if debug:
        print("Response message content:")
        print(response_message.content)
    
    # If function call in the response
    if "get_storybook_illustration" in response_message.content:
        # Notify the user that the process is running in the background
        await cl.Message(content="Generating your storybook and audio narration, please wait...").send()

        # Define the blocking part of the function
        def generate_pdf_and_audio():
            try:
                if debug:
                    print(f"Attempting to parse response content: {response_message.content}")
                
                # Check if content is empty or invalid
                if not response_message.content or not response_message.content.strip():
                    raise ValueError("Response content is empty")
                
                # Extract JSON from response (in case AI includes extra text)
                content = response_message.content.strip()
                
                # Find the first occurrence of '{' and last occurrence of '}'
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                
                if start_idx == -1 or end_idx == -1:
                    raise ValueError("No valid JSON found in response")
                
                # Extract just the JSON part
                json_content = content[start_idx:end_idx + 1]
                
                if debug:
                    print(f"Extracted JSON content: {json_content}")
                
                x = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
                
                # Validate that we have the required fields
                if not hasattr(x, 'arguments'):
                    raise ValueError("Response does not contain 'arguments' field")
                
                args = x.arguments
                required_fields = ['title', 'characters', 'cover_picture_description', 'num_pages', 'pages']
                for field in required_fields:
                    if not hasattr(args, field):
                        raise ValueError(f"Missing required field: {field}")
                
                # Convert SimpleNamespace objects back to dictionaries for the storybook generator
                characters_dict = [{"character_name": char.character_name, "character_features": char.character_features} for char in args.characters]
                pages_dict = [{"page_num": page.page_num, "page_text": page.page_text, "page_picture_description": page.page_picture_description} for page in args.pages]
                
                # Run the async function and get the result
                story_book_name = asyncio.run(get_storybook_illustration(
                    args.title, 
                    characters_dict, 
                    args.cover_picture_description, 
                    args.num_pages, 
                    pages_dict
                ))
                # The PDF is generated in the project root directory, not in the app directory
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                pdf_file_path = os.path.join(project_root, story_book_name)
                if debug:
                    print("Story book path: " + pdf_file_path)
                
                # Generate audio narration
                from app.services.ai.audio_generator import generate_audio_from_text
                import uuid
                
                # Create audio outputs directory if it doesn't exist
                os.makedirs("audio_outputs", exist_ok=True)
                
                # Combine all story text for audio generation
                story_text = f"Title: {args.title}\n\n"
                for page in args.pages:
                    story_text += f"{page.page_text}\n\n"
                
                # Generate audio file
                audio_file_name = f"story_{uuid.uuid4().hex}.mp3"
                audio_output_path = os.path.join("audio_outputs", audio_file_name)
                
                # Generate audio with dynamic voice styles
                generate_audio_from_text(story_text, audio_output_path, language="en", voice_style=None)
                
                return story_book_name, pdf_file_path, audio_file_name, audio_output_path
                
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse JSON response: {e}. Content: {response_message.content[:200]}..."
                print(error_msg)
                raise ValueError(error_msg)
            except Exception as e:
                error_msg = f"Error in generate_pdf_and_audio: {e}"
                print(error_msg)
                raise ValueError(error_msg)

        # Function to send the PDF and audio once they're generated
        async def send_pdf_and_audio(story_book_name, pdf_file_path, audio_file_name, audio_output_path):
            try:
                # Send PDF
                new_response_message = await cl.Message(content=f"Here is your storybook: {story_book_name}").send()
                await cl.File(
                    name=story_book_name,
                    content=open(pdf_file_path, "rb").read(),
                    mime_type="application/pdf"
                ).send(for_id=new_response_message.id)
                
                # Send audio
                audio_message = await cl.Message(content="🎵 Here's the audio narration with expressive voice styles!").send()
                await cl.File(
                    name=audio_file_name,
                    content=open(audio_output_path, "rb").read(),
                    mime_type="audio/mpeg"
                ).send(for_id=audio_message.id)
                
            except Exception as e:
                error_msg = f"Error sending files: {e}"
                print(error_msg)
                await cl.Message(content=f"Sorry, there was an error generating your storybook or audio: {str(e)}").send()

        # Use a ThreadPoolExecutor to run the blocking function in a separate thread
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor()
        future = loop.run_in_executor(executor, generate_pdf_and_audio)

        # Schedule the send_pdf_and_audio coroutine to run once the future is done
        def handle_result(future):
            try:
                result = future.result()
                asyncio.run_coroutine_threadsafe(send_pdf_and_audio(*result), loop)
            except Exception as e:
                error_msg = f"Error in generation callback: {e}"
                print(error_msg)
                asyncio.run_coroutine_threadsafe(
                    cl.Message(content=f"Sorry, there was an error generating your storybook: {str(e)}").send(), 
                    loop
                )
        
        future.add_done_callback(handle_result)
    else:
        message_history.append({"role": "assistant", "content": response_message.content})
    
    if debug:
        print("Message history:")
        print(message_history)
    cl.user_session.set("message_history", message_history)

async def send_audio_file(audio_file_name, audio_output_path):
    """Send audio file to the user."""
    try:
        audio_message = await cl.Message(content="🎵 Here's the audio narration with expressive voice styles!").send()
        await cl.File(
            name=audio_file_name,
            content=open(audio_output_path, "rb").read(),
            mime_type="audio/mpeg"
        ).send(for_id=audio_message.id)
    except Exception as e:
        error_msg = f"Error sending audio file: {e}"
        print(error_msg)
        await cl.Message(content=f"Sorry, there was an error sending the audio file: {str(e)}").send()

if __name__ == "__main__":
    cl.run() 