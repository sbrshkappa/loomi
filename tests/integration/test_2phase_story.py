#!/usr/bin/env python3
"""
Test script for the 2-phase story creation approach.
This demonstrates the interactive planning and final generation process.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_2phase_story_creation():
    """Test the complete 2-phase story creation process."""
    
    print("🎭 Testing 2-Phase Story Creation Process")
    print("=" * 50)
    
    # Phase 1: Interactive Story Planning
    print("\n📝 Phase 1: Interactive Story Planning")
    print("-" * 40)
    
    # Start planning session
    planning_data = {
        "messages": [
            {
                "role": "user",
                "content": "I want to create a story about a little girl who discovers a magical garden in her backyard"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/plan-story", json=planning_data)
    if response.status_code != 200:
        print(f"❌ Planning failed: {response.text}")
        return
    
    planning_response = response.json()
    session_id = planning_response["session_id"]
    print(f"✅ Planning session started: {session_id}")
    print(f"🤖 AI Response: {planning_response['response'][:200]}...")
    
    # Continue planning conversation
    planning_data = {
        "messages": [
            {
                "role": "user",
                "content": "Her name is Lily and she's 5 years old. She loves flowers and animals."
            }
        ],
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/plan-story", json=planning_data)
    if response.status_code == 200:
        planning_response = response.json()
        print(f"🤖 AI Response: {planning_response['response'][:200]}...")
    
    # Continue planning
    planning_data = {
        "messages": [
            {
                "role": "user",
                "content": "The garden should have talking flowers and a wise old tree. Maybe she learns about friendship."
            }
        ],
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/plan-story", json=planning_data)
    if response.status_code == 200:
        planning_response = response.json()
        print(f"🤖 AI Response: {planning_response['response'][:200]}...")
    
    # Phase 2: Generate Final Story
    print("\n🎬 Phase 2: Generate Final Story")
    print("-" * 40)
    
    # Generate audio story
    print("🎵 Generating audio story...")
    response = requests.post(
        f"{BASE_URL}/generate-story?output_type=audio",
        params={"session_id": session_id}
    )
    
    if response.status_code != 200:
        print(f"❌ Story generation failed: {response.text}")
        return
    
    story_response = response.json()
    print(f"✅ Story generated successfully!")
    print(f"📖 Story preview: {story_response['response'][:300]}...")
    
    if story_response.get("audio_url"):
        print(f"🎵 Audio URL: {story_response['audio_url']}")
        print(f"🔗 Full audio URL: {BASE_URL}{story_response['audio_url']}")
    else:
        print("⚠️ No audio URL generated")
    
    # Generate PDF storybook
    print("\n📚 Generating PDF storybook...")
    response = requests.post(
        f"{BASE_URL}/generate-story?output_type=pdf",
        params={"session_id": session_id}
    )
    
    if response.status_code == 200:
        pdf_response = response.json()
        print(f"✅ PDF storybook generated!")
        if pdf_response.get("storybook_name"):
            print(f"📖 PDF URL: {BASE_URL}/storybook/{pdf_response['storybook_name']}")
    
    # Get session history
    print(f"\n📋 Session History")
    print("-" * 40)
    response = requests.get(f"{BASE_URL}/sessions/{session_id}/history")
    if response.status_code == 200:
        history = response.json()
        print(f"Session has {len(history['history'])} messages")
        for i, msg in enumerate(history['history'][:6]):  # Show first 6 messages
            role = msg['role']
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"{i+1}. {role}: {content}")
    
    print("\n🎉 2-Phase Story Creation Complete!")
    print("=" * 50)

def test_direct_story_generation():
    """Test direct story generation for comparison."""
    
    print("\n🚀 Testing Direct Story Generation (for comparison)")
    print("-" * 50)
    
    # Direct story generation
    story_data = {
        "messages": [
            {
                "role": "user",
                "content": "Tell me a story about a brave little mouse who discovers a magical cheese factory"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/story?output_type=audio", json=story_data)
    if response.status_code == 200:
        direct_response = response.json()
        print(f"✅ Direct story generated!")
        print(f"📖 Story preview: {direct_response['response'][:200]}...")
        if direct_response.get("audio_url"):
            print(f"🎵 Audio URL: {direct_response['audio_url']}")
    else:
        print(f"❌ Direct generation failed: {response.text}")

if __name__ == "__main__":
    try:
        test_2phase_story_creation()
        test_direct_story_generation()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}") 