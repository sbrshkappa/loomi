#!/usr/bin/env python3
"""
Simple Audio Generation Test
Test if the audio generation service is working properly
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_audio_generation():
    """Test the audio generation service"""
    print("🎵 Testing Audio Generation Service")
    print("=" * 40)
    
    try:
        # Test 1: Import audio generator
        print("\n1. Testing audio generator import...")
        from app.services.ai.audio_generator import generate_audio_from_text
        print("✅ Audio generator imported successfully")
        
        # Test 2: Simple text generation
        print("\n2. Testing simple audio generation...")
        test_text = "Hello, this is a test story for audio generation. It's a simple story about a bear and a boy who become friends."
        
        # Create output directory
        os.makedirs("audio_outputs", exist_ok=True)
        output_path = "audio_outputs/test_story.mp3"
        
        # Generate audio
        result = generate_audio_from_text(test_text, output_path)
        print(f"✅ Audio generated successfully: {result}")
        
        # Check if file exists
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Audio file created: {output_path} ({file_size} bytes)")
        else:
            print(f"❌ Audio file not found: {output_path}")
        
        print("\n🎉 Audio generation test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Audio generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_generation()
    sys.exit(0 if success else 1) 