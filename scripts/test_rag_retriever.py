#!/usr/bin/env python3
"""
Test RAG Retriever
Demonstrates the retriever functionality with various queries
"""

import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "app"))

from services.rag.retriever import RAGRetriever

def test_retriever():
    """Test the RAG retriever with various queries"""
    print("🔍 Testing RAG Retriever")
    print("=" * 50)
    
    # Initialize retriever
    retriever = RAGRetriever()
    
    # Test queries
    test_queries = [
        "brave lion",
        "friendship and loyalty", 
        "honesty and truth",
        "hard work pays off",
        "clever fox",
        "kindness to others"
    ]
    
    print("\n📚 Testing Basic Retrieval:")
    print("-" * 30)
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        stories = retriever.retrieve_relevant_stories(query, n_results=2)
        
        if stories:
            for i, story in enumerate(stories, 1):
                print(f"  {i}. {story.title} (similarity: {story.similarity_score:.3f})")
                print(f"     Moral: {story.moral}")
                if story.themes:
                    print(f"     Themes: {', '.join(story.themes)}")
        else:
            print("  No relevant stories found")
    
    # Test specialized retrieval methods
    print("\n🎯 Testing Specialized Retrieval:")
    print("-" * 35)
    
    # Test theme retrieval
    print("\n📖 Theme-based retrieval:")
    theme_stories = retriever.retrieve_by_theme("courage", n_results=2)
    for story in theme_stories:
        print(f"  • {story.title} (similarity: {story.similarity_score:.3f})")
    
    # Test character retrieval
    print("\n🐾 Character-based retrieval:")
    character_stories = retriever.retrieve_by_character("fox", n_results=2)
    for story in character_stories:
        print(f"  • {story.title} (similarity: {story.similarity_score:.3f})")
    
    # Test moral retrieval
    print("\n💡 Moral-based retrieval:")
    moral_stories = retriever.retrieve_by_moral("honesty", n_results=2)
    for story in moral_stories:
        print(f"  • {story.title} (similarity: {story.similarity_score:.3f})")
    
    # Test age group retrieval
    print("\n👶 Age group retrieval:")
    age_stories = retriever.retrieve_by_age_group("5-8", "animals", n_results=2)
    for story in age_stories:
        print(f"  • {story.title} (age: {story.age_group}, similarity: {story.similarity_score:.3f})")
    
    # Test smart retrieval
    print("\n🧠 Testing Smart Retrieval:")
    print("-" * 30)
    
    smart_query = "brave lion who helps others"
    smart_result = retriever.smart_retrieve(smart_query, n_results=3)
    
    print(f"Query: '{smart_query}'")
    print(f"Retrieved {smart_result['retrieved_count']} stories")
    
    context = smart_result['context']
    print(f"Context - Themes: {context.get('themes', [])}")
    print(f"Context - Characters: {context.get('characters', [])}")
    print(f"Context - Age Group: {context.get('age_group', 'Unknown')}")
    print(f"Context - Average Similarity: {context.get('avg_similarity', 0):.3f}")
    
    # Show prompt addition
    print("\n📝 Generated Prompt Addition:")
    print("-" * 35)
    print(smart_result['prompt_addition'])
    
    # Test story context extraction
    print("\n🔍 Story Context Analysis:")
    print("-" * 30)
    
    if smart_result['stories']:
        context = retriever.get_story_context(smart_result['stories'])
        print(f"Common themes: {context.get('themes', [])}")
        print(f"Common characters: {context.get('characters', [])}")
        print(f"Morals found: {len(context.get('morals', []))}")
        print(f"Target age group: {context.get('age_group', 'Unknown')}")
    
    print("\n✅ RAG Retriever Test Complete!")
    print("\n🎯 Key Features Demonstrated:")
    print("   • Basic semantic search")
    print("   • Theme-based retrieval")
    print("   • Character-based retrieval")
    print("   • Moral-based retrieval")
    print("   • Age-appropriate filtering")
    print("   • Smart multi-strategy retrieval")
    print("   • Context extraction")
    print("   • Prompt formatting")

if __name__ == "__main__":
    test_retriever() 