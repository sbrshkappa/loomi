#!/usr/bin/env python3
"""
Test script to demonstrate enhanced audio prompts for story generation.
This script shows the difference between regular and audio-optimized story generation.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
import openai

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.prompts.story_prompts import SYSTEM_PROMPT, IMAGE_GENERATION_PROMPT
from app.core.prompts.audio_prompts import AUDIO_STORY_PROMPT, AUDIO_STORYBOOK_PROMPT
from app.config.settings import get_configuration, get_generation_kwargs

# Load environment variables
load_dotenv()

async def test_story_generation():
    """Test both regular and audio-optimized story generation."""
    
    # Get configuration
    config = get_configuration()
    gen_kwargs = get_generation_kwargs()
    
    # Initialize OpenAI client
    client = openai.AsyncClient(
        api_key=config["api_key"], 
        base_url=config["endpoint_url"]
    )
    
    # Test prompt
    test_prompt = "Tell me a story about a brave little mouse who goes on an adventure"
    
    print("=" * 80)
    print("TESTING STORY GENERATION PROMPTS")
    print("=" * 80)
    
    # Test 1: Regular story generation
    print("\n1. REGULAR STORY GENERATION")
    print("-" * 40)
    
    regular_messages = [
        {"role": "system", "content": SYSTEM_PROMPT + IMAGE_GENERATION_PROMPT},
        {"role": "user", "content": test_prompt}
    ]
    
    try:
        response = await client.chat.completions.create(
            messages=regular_messages,
            stream=False,
            **gen_kwargs
        )
        
        regular_story = response.choices[0].message.content
        print("Regular Story Response:")
        print(regular_story[:500] + "..." if len(regular_story) > 500 else regular_story)
        
    except Exception as e:
        print(f"Error generating regular story: {e}")
    
    # Test 2: Audio-optimized story generation
    print("\n\n2. AUDIO-OPTIMIZED STORY GENERATION")
    print("-" * 40)
    
    audio_messages = [
        {"role": "system", "content": AUDIO_STORY_PROMPT + AUDIO_STORYBOOK_PROMPT},
        {"role": "user", "content": test_prompt}
    ]
    
    try:
        response = await client.chat.completions.create(
            messages=audio_messages,
            stream=False,
            **gen_kwargs
        )
        
        audio_story = response.choices[0].message.content
        print("Audio-Optimized Story Response:")
        print(audio_story[:500] + "..." if len(audio_story) > 500 else audio_story)
        
    except Exception as e:
        print(f"Error generating audio story: {e}")
    
    # Test 3: Compare the differences
    print("\n\n3. KEY DIFFERENCES")
    print("-" * 40)
    print("Audio-optimized stories should include:")
    print("• More sensory details (sounds, textures, smells)")
    print("• Enhanced emotional expressions")
    print("• Natural speech patterns and rhythm")
    print("• Character voice distinctions")
    print("• Immersive atmospheric details")
    print("• Onomatopoeia and sound words")
    print("• Interactive elements for listeners")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_story_generation()) 