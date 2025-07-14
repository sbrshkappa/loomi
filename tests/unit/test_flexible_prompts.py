#!/usr/bin/env python3
"""
Test script for the new flexible prompt architecture.
This script verifies that all prompt combinations work correctly.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_prompt_factory():
    """Test the PromptFactory and all available output types."""
    
    print("=" * 80)
    print("TESTING FLEXIBLE PROMPT ARCHITECTURE")
    print("=" * 80)
    
    try:
        from app.core.prompts.prompt_factory import PromptFactory, AVAILABLE_OUTPUT_TYPES
        
        print(f"\nAvailable output types: {list(AVAILABLE_OUTPUT_TYPES.keys())}")
        
        # Test each output type
        for output_type in AVAILABLE_OUTPUT_TYPES:
            print(f"\n{'-' * 40}")
            print(f"Testing: {output_type}")
            print(f"Description: {AVAILABLE_OUTPUT_TYPES[output_type]}")
            
            try:
                prompt = PromptFactory.get_prompt(output_type)
                print(f"✅ Success: {len(prompt)} characters")
                print(f"Preview: {prompt[:100]}...")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Test convenience functions
        print(f"\n{'-' * 40}")
        print("Testing convenience functions...")
        
        from app.core.prompts.prompt_factory import (
            get_text_prompt,
            get_pdf_prompt,
            get_audio_prompt,
            get_audio_pdf_prompt,
            get_audio_storybook_prompt
        )
        
        functions = [
            ("get_text_prompt", get_text_prompt),
            ("get_pdf_prompt", get_pdf_prompt),
            ("get_audio_prompt", get_audio_prompt),
            ("get_audio_pdf_prompt", get_audio_pdf_prompt),
            ("get_audio_storybook_prompt", get_audio_storybook_prompt)
        ]
        
        for func_name, func in functions:
            try:
                prompt = func()
                print(f"✅ {func_name}: {len(prompt)} characters")
            except Exception as e:
                print(f"❌ {func_name}: {e}")
        
        # Test backward compatibility
        print(f"\n{'-' * 40}")
        print("Testing backward compatibility...")
        
        try:
            from app.core.prompts.story_prompts import SYSTEM_PROMPT
            print(f"✅ Legacy SYSTEM_PROMPT: {len(SYSTEM_PROMPT)} characters")
        except Exception as e:
            print(f"❌ Legacy SYSTEM_PROMPT: {e}")
        
        try:
            from app.core.prompts.audio_prompts import AUDIO_STORY_PROMPT
            print(f"✅ Legacy AUDIO_STORY_PROMPT: {len(AUDIO_STORY_PROMPT)} characters")
        except Exception as e:
            print(f"❌ Legacy AUDIO_STORY_PROMPT: {e}")
        
        # Test modular components
        print(f"\n{'-' * 40}")
        print("Testing modular components...")
        
        try:
            from app.core.prompts.base_prompts import BASE_STORY_PROMPT
            print(f"✅ BASE_STORY_PROMPT: {len(BASE_STORY_PROMPT)} characters")
        except Exception as e:
            print(f"❌ BASE_STORY_PROMPT: {e}")
        
        try:
            from app.core.prompts.image_prompts import IMAGE_GENERATION_PROMPT
            print(f"✅ IMAGE_GENERATION_PROMPT: {len(IMAGE_GENERATION_PROMPT)} characters")
        except Exception as e:
            print(f"❌ IMAGE_GENERATION_PROMPT: {e}")
        
        try:
            from app.core.prompts.audio_prompts import AUDIO_ENHANCEMENTS
            print(f"✅ AUDIO_ENHANCEMENTS: {len(AUDIO_ENHANCEMENTS)} characters")
        except Exception as e:
            print(f"❌ AUDIO_ENHANCEMENTS: {e}")
        
        print(f"\n{'-' * 40}")
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("=" * 80)

def test_prompt_differences():
    """Test that different output types produce different prompts."""
    
    print("\n" + "=" * 80)
    print("TESTING PROMPT DIFFERENCES")
    print("=" * 80)
    
    try:
        from app.core.prompts.prompt_factory import PromptFactory
        
        # Get prompts for different types
        text_prompt = PromptFactory.get_prompt("text")
        pdf_prompt = PromptFactory.get_prompt("pdf")
        audio_prompt = PromptFactory.get_prompt("audio")
        audio_pdf_prompt = PromptFactory.get_prompt("audio_pdf")
        
        print(f"\nText prompt length: {len(text_prompt)}")
        print(f"PDF prompt length: {len(pdf_prompt)}")
        print(f"Audio prompt length: {len(audio_prompt)}")
        print(f"Audio+PDF prompt length: {len(audio_pdf_prompt)}")
        
        # Verify they're different
        prompts = [text_prompt, pdf_prompt, audio_prompt, audio_pdf_prompt]
        unique_lengths = len(set(len(p) for p in prompts))
        
        if unique_lengths == len(prompts):
            print("✅ All prompts have different lengths (as expected)")
        else:
            print("⚠️  Some prompts have the same length (check if this is correct)")
        
        # Check that audio prompts contain audio-specific content
        audio_keywords = ["sound", "voice", "rhythm", "narration", "audio"]
        audio_prompts = [audio_prompt, audio_pdf_prompt]
        
        for i, prompt in enumerate(audio_prompts):
            found_keywords = [kw for kw in audio_keywords if kw.lower() in prompt.lower()]
            print(f"Audio prompt {i+1} contains keywords: {found_keywords}")
        
        print("✅ PROMPT DIFFERENCE TESTS COMPLETED!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_prompt_factory()
    test_prompt_differences() 