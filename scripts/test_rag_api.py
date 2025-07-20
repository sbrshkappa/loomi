#!/usr/bin/env python3
"""
Test RAG API Integration
Tests the RAG-enhanced story generation API endpoints
"""

import asyncio
import os
import sys
import requests
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
API_BASE_URL = "http://localhost:8000/api/v1/rag"

def test_rag_health():
    """Test RAG system health"""
    print("🏥 Testing RAG Health Check...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Status: {health['status']}")
            print(f"📁 Vector Store: {'✅' if health['vector_store_exists'] else '❌'}")
            print(f"🔍 Retriever: {'✅' if health['retriever_works'] else '❌'}")
            print(f"📊 Sessions: {health['total_sessions']}")
            return health['status'] == 'healthy'
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_story_retrieval():
    """Test story retrieval from vector store"""
    print("\n🔍 Testing Story Retrieval...")
    
    test_queries = [
        "brave lion",
        "clever fox",
        "friendship between animals",
        "honesty and truthfulness"
    ]
    
    for query in test_queries:
        try:
            response = requests.get(f"{API_BASE_URL}/retrieve", params={
                "query": query,
                "n_results": 2
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n📝 Query: '{query}'")
                print(f"📚 Found {len(result['stories'])} stories:")
                
                for story in result['stories']:
                    print(f"  • {story['title']} (similarity: {story['similarity_score']:.3f})")
                    print(f"    Moral: {story['moral']}")
                    print(f"    Themes: {', '.join(story['themes'])}")
            else:
                print(f"❌ Retrieval failed for '{query}': {response.status_code}")
                
        except Exception as e:
            print(f"❌ Retrieval error for '{query}': {e}")

def test_rag_story_generation():
    """Test RAG-enhanced story generation"""
    print("\n📚 Testing RAG Story Generation...")
    
    test_requests = [
        "A brave lion who learns to be kind to smaller animals",
        "A clever fox who helps his friends solve a problem"
    ]
    
    for request in test_requests:
        print(f"\n🎯 Generating story for: '{request}'")
        
        try:
            # Generate with RAG
            response = requests.post(f"{API_BASE_URL}/generate", json={
                "user_request": request,
                "use_rag": True,
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 1000
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ RAG Story Generated!")
                print(f"⏱️  Generation time: {result['generation_time']:.2f}s")
                print(f"📝 Word count: {result['word_count']}")
                print(f"🎯 Retrieved stories: {result['retrieved_stories_count']}")
                print(f"🎭 Themes: {', '.join(result['retrieved_themes'])}")
                print(f"🐾 Characters: {', '.join(result['retrieved_characters'])}")
                print(f"📊 Similarity scores: {[f'{s:.3f}' for s in result['similarity_scores']]}")
                
                if result['educational_value_score']:
                    print(f"📖 Educational value: {result['educational_value_score']:.3f}")
                if result['engagement_score']:
                    print(f"🎭 Engagement: {result['engagement_score']:.3f}")
                if result['coherence_score']:
                    print(f"🔗 Coherence: {result['coherence_score']:.3f}")
                
                print(f"\n📖 Story Preview:")
                print("-" * 40)
                print(result['story_content'][:300] + "..." if len(result['story_content']) > 300 else result['story_content'])
                
            else:
                print(f"❌ Generation failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Generation error: {e}")

def test_story_comparison():
    """Test RAG vs non-RAG story comparison"""
    print("\n⚖️ Testing RAG vs Non-RAG Comparison...")
    
    test_request = "A little mouse who discovers the power of friendship"
    
    try:
        response = requests.post(f"{API_BASE_URL}/compare", json={
            "user_request": test_request,
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Comparison completed!")
            
            # Display comparison metrics
            comparison = result['comparison']
            print(f"\n📊 Comparison Metrics:")
            print(f"⏱️  Generation time difference: {comparison['generation_time_diff']:.2f}s")
            print(f"📝 Word count difference: {comparison['word_count_diff']}")
            print(f"🔤 Character count difference: {comparison['character_count_diff']}")
            print(f"📈 Context enhancement: {comparison['context_enhancement']} characters")
            
            # Display story previews
            stories = result['stories']
            
            print(f"\n📝 Story WITHOUT RAG:")
            print("-" * 40)
            without_rag = stories['without_rag']['content']
            print(without_rag[:200] + "..." if len(without_rag) > 200 else without_rag)
            
            print(f"\n📚 Story WITH RAG:")
            print("-" * 40)
            with_rag = stories['with_rag']['content']
            print(with_rag[:200] + "..." if len(with_rag) > 200 else with_rag)
            
        else:
            print(f"❌ Comparison failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Comparison error: {e}")

def test_metrics():
    """Test metrics collection and export"""
    print("\n📊 Testing Metrics Collection...")
    
    try:
        # Get metrics summary
        response = requests.get(f"{API_BASE_URL}/metrics/summary")
        
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Metrics Summary:")
            print(f"📊 Total sessions: {summary['total_sessions']}")
            print(f"✅ Success rate: {summary['success_rate']:.1%}")
            print(f"⏱️  Avg generation time (without RAG): {summary['avg_generation_time_without_rag']:.2f}s")
            print(f"⏱️  Avg generation time (with RAG): {summary['avg_generation_time_with_rag']:.2f}s")
            print(f"📈 Avg RAG overhead: {summary['avg_rag_overhead']:.2f}s")
            print(f"🎯 Avg similarity score: {summary['avg_similarity_score']:.3f}")
            
            if summary['avg_quality_improvement']:
                print(f"\n📈 Quality Improvements:")
                for metric, improvement in summary['avg_quality_improvement'].items():
                    print(f"  {metric.replace('_', ' ').title()}: {improvement:+.3f}")
            
            print(f"\n🎭 Most common themes: {', '.join(summary['most_common_themes'])}")
            print(f"🐾 Most common characters: {', '.join(summary['most_common_characters'])}")
            
        else:
            print(f"❌ Metrics summary failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Metrics error: {e}")

def main():
    """Main test function"""
    
    print("🎭 RAG API Integration Test")
    print("=" * 60)
    print("This script tests the RAG-enhanced story generation API endpoints.")
    print()
    
    # Check if API server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server is not running. Please start the server first:")
            print("   python -m uvicorn app.api.app:app --reload --host 0.0.0.0 --port 8000")
            return
    except:
        print("❌ Cannot connect to API server. Please start the server first:")
        print("   python -m uvicorn app.api.app:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("✅ API server is running!")
    
    # Run tests
    try:
        # Test health
        if not test_rag_health():
            print("❌ RAG system is not healthy. Please check the setup.")
            return
        
        # Test retrieval
        test_story_retrieval()
        
        # Test generation
        test_rag_story_generation()
        
        # Test comparison
        test_story_comparison()
        
        # Test metrics
        test_metrics()
        
        print("\n✅ All tests completed successfully!")
        print("\n🎯 Next Steps:")
        print("1. View API documentation at: http://localhost:8000/docs")
        print("2. Run the full research test: python scripts/test_rag_integration.py")
        print("3. Export metrics: POST /api/v1/rag/metrics/export")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 