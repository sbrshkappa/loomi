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
import time
from datetime import datetime
from types import SimpleNamespace
from typing import Any

from dotenv import load_dotenv
import chainlit as cl
import openai

from app.config.settings import get_configuration
from app.core.prompts.story_prompts import SYSTEM_PROMPT, IMAGE_GENERATION_PROMPT, AUDIO_OPTIMIZED_PROMPT
from app.core.prompts.base_prompts import BASE_STORY_PROMPT
from app.services.ai.storybook_generator import get_storybook_illustration
from app.utils.helpers import get_latest_user_message
from app.research.tracing import ResearchTracer
from app.services.rag.integration import RAGIntegration
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

# Initialize research tracer
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
research_tracer = ResearchTracer(langsmith_api_key)

# Initialize RAG integration
rag_integration = RAGIntegration()

# RAG toggle flag - set to True to enable RAG enhancement
ENABLE_RAG = os.getenv("ENABLE_RAG", "false").lower() == "true"

@traceable
@cl.on_chat_start
async def on_chat_start():    
    """Initialize chat session with conversational story creation flow."""
    # Initialize conversation state
    conversation_state = {
        "stage": "greeting",  # greeting, gathering_info, generating
        "story_requirements": {
            "age": None,
            "theme": None,
            "characters": None,
            "length": None,
            "format": None  # audio, pdf, both
        },
        "message_history": []
    }
    
    cl.user_session.set("conversation_state", conversation_state)
    
    # Send initial greeting
    greeting_message = """🎭 **Welcome to Loomi - Your AI Storytelling Companion!**

I'm here to create personalized stories just for you! 

**What would you like to do today?**
- 📖 Create a new story
- 🎵 Generate audio narration
- 📚 Make a storybook with illustrations
- 🎭 All of the above!

Just tell me what you'd like, and I'll guide you through the process!"""
    
    await cl.Message(content=greeting_message).send()

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
    """Check if the user is requesting audio generation for an existing story."""
    # Keywords that specifically request audio for existing content
    audio_only_keywords = [
        "read aloud", "narrate", "play audio", "generate audio", 
        "create audio", "make audio", "audio version"
    ]
    
    # Keywords that might mean "hear a new story" vs "hear existing story"
    ambiguous_keywords = [
        "listen", "hear", "voice", "speak", "sound", "recording"
    ]
    
    message_lower = user_message.lower()
    
    # If it's clearly an audio-only request, return True
    if any(keyword in message_lower for keyword in audio_only_keywords):
        return True
    
    # For ambiguous keywords, check if there's context suggesting a new story request
    if any(keyword in message_lower for keyword in ambiguous_keywords):
        # If the message contains story creation keywords, it's likely a new story request
        story_creation_keywords = ["story", "tale", "narrative", "about", "teaches", "importance"]
        if any(keyword in message_lower for keyword in story_creation_keywords):
            return False  # This is a new story request, not audio-only
        return True  # This is likely an audio request for existing content
    
    return False

@traceable
@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages with AI-driven conversational story creation flow."""
    
    # Check for research export command first
    if message.content.lower().strip() == "export research":
        if research_tracer.sessions:
            export_result = research_tracer.export_metrics()
            await cl.Message(content=f"📊 Research metrics exported!\n\nFiles created:\n- Raw data: {export_result['raw_data_file']}\n- Aggregate metrics: {export_result['aggregate_file']}\n- Research report: {export_result['report_file']}\n\nTotal sessions tracked: {len(research_tracer.sessions)}").send()
        else:
            await cl.Message(content="No research data collected yet. Generate some stories first!").send()
        return
    
    # Get conversation state
    conversation_state = cl.user_session.get("conversation_state", {})
    message_history = conversation_state.get("message_history", [])
    
    # Add user message to history
    message_history.append({"role": "user", "content": message.content})
    
    # Use AI to handle the entire conversation flow
    response, new_state, should_generate, rag_enhancement_result = await handle_conversation_with_ai(message.content, conversation_state, message_history)
    
    # Update conversation state
    conversation_state.update(new_state)
    conversation_state["message_history"] = message_history
    cl.user_session.set("conversation_state", conversation_state)
    
    # Note: The response is already sent by generate_response function, so we don't send it again here
    
    # If AI determined we should generate a story, start the process
    if should_generate:
        if debug:
            print(f"Starting story generation with format: {conversation_state.get('story_requirements', {}).get('format', 'both')}")
            print(f"Story response: {response[:200]}...")
        # Extract the story from the AI response and generate audio/PDF
        await start_story_generation(conversation_state["story_requirements"], message_history, response, rag_enhancement_result)

    if debug:
        print("Message history:")
        print(message_history)

async def handle_conversation_with_ai(user_message: str, conversation_state: dict, message_history: list) -> tuple[str, dict, bool, Any]:
    """AI-driven conversation handler that manages the entire story creation flow."""
    
    # Create a comprehensive prompt for the AI to understand and respond
    system_prompt = """You are Loomi, an AI storytelling assistant. Your job is to help users create personalized stories.

**Your Process:**
1. **Understand Intent:** Determine if user wants a new story, audio, or both
2. **Extract Information:** Pull out age, theme, characters, format preferences from what the user explicitly says
3. **Ask Questions:** If information is missing, ask specific, friendly questions
4. **Generate Story:** When you have enough info, write the complete story and end with "READY_TO_GENERATE"

**Information to Collect:**
- Age of the child (for age-appropriate content)
- Theme/lesson (friendship, sharing, bravery, etc.)
- Characters (animals, children, fantasy creatures, etc.)
- Format preference (audio only, storybook only, or both)

**Response Guidelines:**
- Be warm, enthusiastic, and child-friendly
- Ask one question at a time
- Acknowledge what you've learned
- **WHEN READY TO GENERATE:** Write the complete story content, then end with "READY_TO_GENERATE"
- **IMPORTANT: Provide only ONE response. Do not repeat yourself or duplicate content.**
- **CRITICAL: Only extract information that the user explicitly mentions. Do not assume themes or characters.**

**Story Generation:**
When you have all the information needed, write a complete, engaging story appropriate for the child's age. Include:
- A catchy title
- Engaging characters and plot
- Age-appropriate language and length
- The requested theme/lesson
- A satisfying ending

**Current Conversation State:**
{conversation_state}

**Recent Messages:**
{recent_messages}

**User's Latest Message:**
{user_message}

Respond naturally as Loomi. If you need more information, ask questions. If you have enough information, write the complete story and end with "READY_TO_GENERATE"."""
    
    # Format the prompt
    recent_messages = message_history[-5:] if message_history else []  # Last 5 messages for context
    formatted_prompt = system_prompt.format(
        conversation_state=json.dumps(conversation_state, indent=2),
        recent_messages=json.dumps(recent_messages, indent=2),
        user_message=user_message
    )
    
    # Apply RAG enhancement if enabled
    rag_enhancement_result = None
    if ENABLE_RAG:
        enhanced_prompt, rag_enhancement_result = rag_integration.enhance_system_prompt(
            formatted_prompt, 
            user_message, 
            conversation_state
        )
        if rag_enhancement_result.enhancement_metadata.get("rag_enabled", False):
            formatted_prompt = enhanced_prompt
            if debug:
                print(f"RAG enhancement applied: {rag_enhancement_result.enhancement_metadata['retrieved_stories_count']} stories retrieved")
    
    # Get AI response
    ai_messages = [
        {"role": "system", "content": formatted_prompt},
        {"role": "user", "content": user_message}
    ]
    
    response = await generate_response(client, ai_messages, gen_kwargs)
    ai_response = response.content
    
    # Check if AI wants to generate a story
    should_generate = "READY_TO_GENERATE" in ai_response
    if debug:
        print(f"Should generate: {should_generate}")
        print(f"AI response contains READY_TO_GENERATE: {'READY_TO_GENERATE' in ai_response}")
    if should_generate:
        ai_response = ai_response.replace("READY_TO_GENERATE", "").strip()
    
    # Let the AI manage the conversation state entirely - no deterministic extraction
    # The AI will naturally gather information through the conversation flow
    new_state = conversation_state.copy()
    
    # Extract format preference from the conversation context
    message_lower = user_message.lower()
    if any(word in message_lower for word in ["audio", "hear", "listen", "narrate"]):
        if any(word in message_lower for word in ["storybook", "pdf", "book", "illustration"]):
            new_state["story_requirements"]["format"] = "both"
        else:
            new_state["story_requirements"]["format"] = "audio"
    elif any(word in message_lower for word in ["storybook", "pdf", "book", "illustration"]):
        new_state["story_requirements"]["format"] = "pdf"
    else:
        new_state["story_requirements"]["format"] = "both"  # Default to both
    
    if debug:
        print(f"Extracted format preference: {new_state['story_requirements']['format']}")
    
    return ai_response, new_state, should_generate, rag_enhancement_result



# Old deterministic functions removed - now using AI for everything

async def start_story_generation(requirements: dict, message_history: list, story_response: str, rag_enhancement_result=None):
    """Start the story generation process using the story from the conversation."""
    # Determine format preference from requirements or conversation context
    format_preference = requirements.get("format", "both")
    
    # Use the story that was already generated in the conversation
    story_content = story_response
    
    # Start research session for tracing
    session_id = research_tracer.start_session()
    
    # Track story generation
    story_start_time = time.time()
    story_end_time = time.time()  # Since story is already generated
    
    if debug:
        print("Story content:")
        print(story_content)
    
    # Determine what to generate based on format preference
    should_generate_pdf = format_preference in ["pdf", "both"] and "get_storybook_illustration" in story_content
    should_generate_audio = format_preference in ["audio", "both"]
    
    # If user wants audio only, always generate audio from the story text
    if format_preference == "audio":
        should_generate_audio = True
    
    if debug:
        print(f"Format preference: {format_preference}")
        print(f"Should generate PDF: {should_generate_pdf}")
        print(f"Should generate audio: {should_generate_audio}")
        print(f"Story content length: {len(story_content)}")
        print(f"Story content preview: {story_content[:100]}...")
    
    # Track story metrics and log to LangSmith immediately
    story_metrics = await research_tracer.trace_story_generation(
        prompt="Story generation from conversation context",
        model=gen_kwargs["model"],
        temperature=gen_kwargs["temperature"],
        max_tokens=gen_kwargs["max_tokens"],
        start_time=story_start_time,
        end_time=story_end_time,
        response_content=story_content
    )
    
    # Add RAG metrics if RAG was used
    if rag_enhancement_result and rag_enhancement_result.enhancement_metadata.get("rag_enabled", False):
        rag_metrics = rag_integration.create_rag_metrics(
            rag_enhancement_result,
            story_end_time - story_start_time,
            story_content,
            gen_kwargs["model"],
            gen_kwargs["temperature"],
            gen_kwargs["max_tokens"]
        )
        if debug:
            print(f"RAG Metrics: {rag_metrics}")
    
    # Log story generation to LangSmith immediately
    await research_tracer._log_story_to_langsmith(story_metrics, story_content)
    
    # Notify the user about what's being generated
    if should_generate_pdf and should_generate_audio:
        await cl.Message(content="Generating your storybook and audio narration, please wait...").send()
    elif should_generate_pdf:
        await cl.Message(content="Generating your storybook with illustrations, please wait...").send()
    elif should_generate_audio:
        await cl.Message(content="Generating your audio narration, please wait...").send()
    
    # Only proceed with generation if we have something to generate
    if should_generate_pdf or should_generate_audio:
        # Define the blocking part of the function
        def generate_content():
            try:
                story_book_name = None
                pdf_file_path = None
                audio_file_name = None
                audio_output_path = None
                image_start_time = None
                image_end_time = None
                audio_start_time = None
                audio_end_time = None
                
                # Use the story content from the conversation
                if debug:
                    print(f"Using story content: {story_content}")
                
                # Check if content is empty or invalid
                if not story_content or not story_content.strip():
                    raise ValueError("Story content is empty")
                
                # Extract story text for audio generation
                story_text = ""
                if should_generate_audio:
                    # For audio, we need to extract the story text from the content
                    # This could be a simple story or from a structured response
                    if "get_storybook_illustration" in story_content:
                        # Extract from structured response
                        content = story_content.strip()
                        start_idx = content.find('{')
                        end_idx = content.rfind('}')
                        
                        if start_idx != -1 and end_idx != -1:
                            json_content = content[start_idx:end_idx + 1]
                            x = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
                            
                            if hasattr(x, 'arguments'):
                                args = x.arguments
                                story_text = f"Title: {args.title}\n\n"
                                for page in args.pages:
                                    story_text += f"{page.page_text}\n\n"
                        else:
                            # Fallback: use the story content as story text
                            story_text = story_content
                    else:
                        # Use the story content directly as story text
                        story_text = story_content
                
                # Generate PDF if requested
                if should_generate_pdf:
                    image_start_time = time.time()
                    
                    # Extract JSON from story content (in case AI includes extra text)
                    content = story_content.strip()
                    
                    # Find the first occurrence of '{' and last occurrence of '}'
                    start_idx = content.find('{')
                    end_idx = content.rfind('}')
                    
                    if start_idx == -1 or end_idx == -1:
                        raise ValueError("No valid JSON found in story content for PDF generation")
                    
                    # Extract just the JSON part
                    json_content = content[start_idx:end_idx + 1]
                    
                    if debug:
                        print(f"Extracted JSON content: {json_content}")
                    
                    x = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
                    
                    # Validate that we have the required fields
                    if not hasattr(x, 'arguments'):
                        raise ValueError("Story content does not contain 'arguments' field")
                    
                    args = x.arguments
                    required_fields = ['title', 'characters', 'cover_picture_description', 'num_pages', 'pages']
                    for field in required_fields:
                        if not hasattr(args, field):
                            raise ValueError(f"Missing required field: {field}")
                    
                    # Convert SimpleNamespace objects back to dictionaries for the storybook generator
                    characters_dict = [{"character_name": char.character_name, "character_features": char.character_features} for char in args.characters]
                    pages_dict = [{"page_num": page.page_num, "page_text": page.page_text, "page_picture_description": page.page_picture_description} for page in args.pages]
                    
                    # Add rate limiting delay for DALL-E
                    time.sleep(10)  # Wait 10 seconds to avoid rate limits
                    
                    # Run the async function and get the result
                    story_book_name = asyncio.run(get_storybook_illustration(
                        args.title, 
                        characters_dict, 
                        args.cover_picture_description, 
                        args.num_pages, 
                        pages_dict
                    ))
                    image_end_time = time.time()
                    
                    # The PDF is generated in the storybooks directory
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    storybooks_dir = os.path.join(project_root, "storybooks")
                    os.makedirs(storybooks_dir, exist_ok=True)
                    pdf_file_path = os.path.join(storybooks_dir, story_book_name)
                    if debug:
                        print("Story book path: " + pdf_file_path)
                        print("Project root: " + project_root)
                        print("Story book name: " + story_book_name)
                        print("PDF file exists: " + str(os.path.exists(pdf_file_path)))
                
                # Generate audio if requested
                if should_generate_audio:
                    audio_start_time = time.time()
                    
                    if debug:
                        print(f"Generating audio from story text (length: {len(story_text)} characters)")
                        print(f"Story text preview: {story_text[:200]}...")
                    
                    # Generate audio narration
                    from app.services.ai.audio_generator import generate_audio_from_text
                    import uuid
                    import re
                    
                    # Create audio outputs directory if it doesn't exist
                    os.makedirs("audio_outputs", exist_ok=True)
                    
                    # Extract story title for filename
                    story_title = "Story"
                    if "get_storybook_illustration" in story_content:
                        # Extract title from structured response
                        try:
                            content = story_content.strip()
                            start_idx = content.find('{')
                            end_idx = content.rfind('}')
                            
                            if start_idx != -1 and end_idx != -1:
                                json_content = content[start_idx:end_idx + 1]
                                x = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
                                
                                if hasattr(x, 'arguments') and hasattr(x.arguments, 'title'):
                                    story_title = x.arguments.title
                        except Exception as e:
                            if debug:
                                print(f"Could not extract title from structured response: {e}")
                    else:
                        # Extract title from simple story text
                        title_match = re.search(r'Title:\s*["\']?([^"\'\n]+)["\']?', story_text, re.IGNORECASE)
                        if title_match:
                            story_title = title_match.group(1)
                        else:
                            # Look for "Title:" at the beginning
                            lines = story_text.split('\n')
                            for line in lines:
                                if line.strip().lower().startswith('title:'):
                                    story_title = line.split(':', 1)[1].strip().strip('"\'')
                                    break
                    
                    # Clean the title for filename (remove special characters, replace spaces with underscores)
                    clean_title = re.sub(r'[^\w\s-]', '', story_title)
                    clean_title = re.sub(r'[-\s]+', '_', clean_title)
                    clean_title = clean_title.strip('_')
                    
                    if not clean_title:
                        clean_title = "Story"
                    
                    # Generate audio file with story title
                    audio_file_name = f"{clean_title}.mp3"
                    audio_output_path = os.path.join("audio_outputs", audio_file_name)
                    
                    # Generate audio with dynamic voice styles
                    generate_audio_from_text(story_text, audio_output_path, language="en", voice_style=None)
                    
                    audio_end_time = time.time()
                    
                    if debug:
                        print(f"Story title extracted: {story_title}")
                        print(f"Clean title for filename: {clean_title}")
                        print(f"Audio generated: {audio_output_path}")
                        print(f"Audio file exists: {os.path.exists(audio_output_path)}")
                
                return story_book_name, pdf_file_path, audio_file_name, audio_output_path, image_start_time, image_end_time, audio_start_time, audio_end_time
                
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse JSON response: {e}. Content: {story_content[:200]}..."
                print(error_msg)
                raise ValueError(error_msg)
            except Exception as e:
                error_msg = f"Error in generate_content: {e}"
                print(error_msg)
                raise ValueError(error_msg)

        # Function to send the generated content
        async def send_generated_content(story_book_name, pdf_file_path, audio_file_name, audio_output_path):
            try:
                # Send PDF if generated
                if story_book_name and pdf_file_path and os.path.exists(pdf_file_path):
                    new_response_message = await cl.Message(content=f"Here is your storybook: {story_book_name}").send()
                    await cl.File(
                        name=story_book_name,
                        content=open(pdf_file_path, "rb").read(),
                        mime_type="application/pdf"
                    ).send(for_id=new_response_message.id)
                elif should_generate_pdf:
                    await cl.Message(content="Sorry, there was an error generating the PDF file.").send()
                
                # Send audio if generated
                if audio_file_name and audio_output_path and os.path.exists(audio_output_path):
                    audio_message = await cl.Message(content="🎵 Here's the audio narration with expressive voice styles!").send()
                    await cl.File(
                        name=audio_file_name,
                        content=open(audio_output_path, "rb").read(),
                        mime_type="audio/mpeg"
                    ).send(for_id=audio_message.id)
                elif should_generate_audio:
                    await cl.Message(content="Sorry, there was an error generating the audio file.").send()
                
            except FileNotFoundError as e:
                error_msg = f"File not found: {e}"
                print(error_msg)
                await cl.Message(content=f"Sorry, there was an error finding the generated files: {str(e)}").send()
            except Exception as e:
                error_msg = f"Error sending files: {e}"
                print(error_msg)
                await cl.Message(content=f"Sorry, there was an error generating your storybook or audio: {str(e)}").send()

        # Use a ThreadPoolExecutor to run the blocking function in a separate thread
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor()
        future = loop.run_in_executor(executor, generate_content)

        # Schedule the send_pdf_and_audio coroutine to run once the future is done
        def handle_result(future):
            try:
                result = future.result()
                # Extract timing data
                story_book_name, pdf_file_path, audio_file_name, audio_output_path, img_start, img_end, aud_start, aud_end = result
                
                # Track image and audio metrics asynchronously
                asyncio.run_coroutine_threadsafe(
                    track_generation_metrics(story_metrics, img_start, img_end, aud_start, aud_end, audio_file_name, audio_output_path),
                    loop
                )
                
                # Send files to user
                asyncio.run_coroutine_threadsafe(send_generated_content(story_book_name, pdf_file_path, audio_file_name, audio_output_path), loop)
            except Exception as e:
                error_msg = f"Error in generation callback: {e}"
                print(error_msg)
                asyncio.run_coroutine_threadsafe(
                    cl.Message(content=f"Sorry, there was an error generating your storybook: {str(e)}").send(), 
                    loop
                )
        
        future.add_done_callback(handle_result)



async def track_generation_metrics(story_metrics, img_start, img_end, aud_start, aud_end, audio_file_name, audio_output_path):
    """Track image and audio generation metrics"""
    try:
        image_metrics = None
        audio_metrics = None
        
        # Track image generation metrics only if PDF was generated
        if img_start is not None and img_end is not None:
            image_metrics = await research_tracer.trace_image_generation(
                story_id=story_metrics.story_id,
                prompt="Story illustration",  # This could be more specific
                model="dall-e-3",
                image_size="1024x1024",
                start_time=img_start,
                end_time=img_end,
                local_path="images/"  # This could be more specific
            )
            
            # Log image generation to LangSmith immediately
            await research_tracer._log_image_to_langsmith(image_metrics)
        
        # Track audio generation metrics only if audio was generated
        if aud_start is not None and aud_end is not None and audio_output_path:
            audio_metrics = await research_tracer.trace_audio_generation(
                story_id=story_metrics.story_id,
                voice_style="dynamic",
                model="openvoice-v2",
                start_time=aud_start,
                end_time=aud_end,
                audio_duration=30.0,  # This could be calculated from the actual audio file
                local_path=audio_output_path
            )
            
            # Log audio generation to LangSmith immediately
            await research_tracer._log_audio_to_langsmith(audio_metrics)
        
        # Complete the research session with available metrics
        research_tracer.complete_session(
            story_metrics=story_metrics,
            image_metrics=[image_metrics] if image_metrics else [],
            audio_metrics=audio_metrics if audio_metrics else None
        )
        
        print(f"✅ Research metrics tracked for session: {research_tracer.current_session_id}")
        
        # Export metrics periodically (every 5 sessions)
        if len(research_tracer.sessions) % 5 == 0:
            export_result = research_tracer.export_metrics()
            print(f"📊 Research metrics exported: {export_result['report_file']}")
        
    except Exception as e:
        print(f"Error tracking metrics: {e}")
        import traceback
        traceback.print_exc()

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