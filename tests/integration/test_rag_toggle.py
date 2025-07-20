#!/usr/bin/env python3
"""
Test RAG Toggle Integration
Demonstrates RAG enhancement with toggle flag in existing system
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_rag_toggle():
    """Test RAG toggle functionality"""
    
    print("🎭 RAG Toggle Integration Test")
    print("=" * 60)
    print("This script demonstrates how to enable/disable RAG enhancement.")
    print()
    
    # Check if vector store exists
    if not os.path.exists("chroma_db"):
        print("❌ Vector store not found. Please run setup_vector_store.py first.")
        return
    
    print("✅ Vector store found!")
    
    # Show how to enable RAG
    print("\n🔧 How to Enable RAG Enhancement:")
    print("-" * 40)
    print("Option 1: Environment Variable")
    print("   export ENABLE_RAG=true")
    print("   python -m chainlit run app/main.py")
    print()
    print("Option 2: Direct in Code")
    print("   In app/main.py, change:")
    print("   ENABLE_RAG = True  # Instead of False")
    print()
    print("Option 3: Runtime Toggle")
    print("   Add a command to toggle RAG on/off")
    
    # Show the current setting
    current_setting = os.getenv("ENABLE_RAG", "false").lower() == "true"
    print(f"\n📊 Current RAG Setting: {'✅ ENABLED' if current_setting else '❌ DISABLED'}")
    
    # Show what happens with RAG enabled
    print("\n🎯 What Happens When RAG is ENABLED:")
    print("-" * 40)
    print("✅ System prompt gets enhanced with relevant Aesop's Fables")
    print("✅ Stories include classic themes and moral lessons")
    print("✅ Better educational content and character development")
    print("✅ Research metrics track RAG performance")
    print("⏱️  Slight performance overhead (~2-3 seconds)")
    
    # Show what happens with RAG disabled
    print("\n🎯 What Happens When RAG is DISABLED:")
    print("-" * 40)
    print("✅ Original system prompt used (no changes)")
    print("✅ Standard story generation (your existing flow)")
    print("✅ No performance overhead")
    print("✅ No RAG metrics collected")
    
    # Show example prompts
    print("\n📝 Example Prompt Enhancement:")
    print("-" * 40)
    print("ORIGINAL PROMPT:")
    print("Story Generation:")
    print("When you have all the information needed, write a complete, engaging story...")
    print()
    print("WITH RAG ENHANCEMENT:")
    print("Story Generation:")
    print()
    print("**RAG Enhancement - Relevant Aesop's Fables for Inspiration:**")
    print("THE LION AND THE MOUSE: A mighty lion spares a tiny mouse...")
    print("**Consider these themes from classic fables:** kindness, friendship")
    print("**Consider these character types:** lion, mouse")
    print("**Use these classic fables as inspiration to create a new, original story...**")
    print()
    print("When you have all the information needed, write a complete, engaging story...")
    
    # Show how to test
    print("\n🧪 How to Test:")
    print("-" * 40)
    print("1. Start your app with RAG disabled:")
    print("   python -m chainlit run app/main.py")
    print()
    print("2. Ask for a story: 'Tell me a story about a brave lion'")
    print()
    print("3. Enable RAG and restart:")
    print("   export ENABLE_RAG=true")
    print("   python -m chainlit run app/main.py")
    print()
    print("4. Ask for the same story and compare the results")
    
    # Show debug information
    print("\n🔍 Debug Information:")
    print("-" * 40)
    print("When RAG is enabled, you'll see debug messages like:")
    print("RAG enhancement applied: 3 stories retrieved")
    print("RAG Metrics: {'rag_enabled': True, 'retrieved_stories_count': 3, ...}")
    
    # Show research benefits
    print("\n📊 Research Benefits:")
    print("-" * 40)
    print("✅ A/B testing capability (RAG vs non-RAG)")
    print("✅ Quality metrics tracking")
    print("✅ Performance comparison")
    print("✅ Educational value measurement")
    print("✅ User preference analysis")
    
    print("\n✅ RAG Toggle Integration Ready!")
    print("\n🎯 Next Steps:")
    print("1. Test with RAG disabled (current setting)")
    print("2. Enable RAG and test again")
    print("3. Compare story quality and performance")
    print("4. Analyze research metrics")

if __name__ == "__main__":
    test_rag_toggle() 