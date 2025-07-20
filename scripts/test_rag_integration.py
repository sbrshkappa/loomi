#!/usr/bin/env python3
"""
Test RAG Integration with Story Generation
Demonstrates RAG-enhanced story generation with research metrics
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import openai

from app.services.rag.story_generator import RAGStoryGenerator
from app.research.rag_metrics import RAGMetricsCollector

# Load environment variables
load_dotenv()

async def test_rag_story_generation():
    """Test RAG-enhanced story generation"""
    
    print("🚀 Testing RAG Integration with Story Generation")
    print("=" * 60)
    
    # Initialize OpenAI client
    client = openai.AsyncClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )
    
    # Initialize RAG story generator
    rag_generator = RAGStoryGenerator(client)
    
    # Initialize metrics collector
    metrics_collector = RAGMetricsCollector()
    
    # Test queries
    test_queries = [
        "A brave lion who learns to be kind to smaller animals",
        "A clever fox who helps his friends solve a problem",
        "A little mouse who discovers the power of friendship",
        "A wise owl who teaches others about sharing",
        "A curious rabbit who learns about patience"
    ]
    
    print(f"\n📊 Running {len(test_queries)} comparison tests...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}/{len(test_queries)} ---")
        print(f"Query: {query}")
        
        try:
            # Start session
            session_id = metrics_collector.start_session()
            
            # Generate comparison stories
            comparison = await rag_generator.generate_comparison_stories(query)
            
            # Record session
            session = metrics_collector.record_comparison_session(
                user_request=query,
                story_without_rag=comparison["stories"]["without_rag"]["content"],
                story_with_rag=comparison["stories"]["with_rag"]["content"],
                metrics_without_rag=comparison["stories"]["without_rag"]["metrics"],
                metrics_with_rag=comparison["stories"]["with_rag"]["metrics"],
                total_time=comparison["stories"]["with_rag"]["metrics"].generation_time
            )
            
            # Display results
            print(f"✅ Session recorded: {session_id}")
            print(f"📝 Without RAG: {comparison['stories']['without_rag']['metrics'].word_count} words")
            print(f"📚 With RAG: {comparison['stories']['with_rag']['metrics'].word_count} words")
            print(f"⏱️  RAG Overhead: {comparison['comparison']['rag_overhead']:.2f}s")
            print(f"🎯 Retrieved stories: {comparison['stories']['with_rag']['metrics'].retrieved_stories_count}")
            
            # Show quality metrics
            if comparison['stories']['with_rag']['metrics'].educational_value_score:
                print(f"📖 Educational value: {comparison['stories']['with_rag']['metrics'].educational_value_score:.3f}")
            
            if comparison['stories']['with_rag']['metrics'].engagement_score:
                print(f"🎭 Engagement: {comparison['stories']['with_rag']['metrics'].engagement_score:.3f}")
            
        except Exception as e:
            print(f"❌ Error in test {i}: {e}")
            continue
    
    # Generate and display research summary
    print("\n" + "=" * 60)
    print("📊 RESEARCH SUMMARY")
    print("=" * 60)
    
    summary = metrics_collector.generate_research_summary()
    
    print(f"Total Sessions: {summary.total_sessions}")
    print(f"Success Rate: {summary.success_rate:.1%}")
    print(f"Average Generation Time (Without RAG): {summary.avg_generation_time_without_rag:.2f}s")
    print(f"Average Generation Time (With RAG): {summary.avg_generation_time_with_rag:.2f}s")
    print(f"Average RAG Overhead: {summary.avg_rag_overhead:.2f}s")
    print(f"Average Similarity Score: {summary.avg_similarity_score:.3f}")
    
    print("\nQuality Improvements:")
    for metric, improvement in summary.avg_quality_improvement.items():
        print(f"  {metric.replace('_', ' ').title()}: {improvement:+.3f}")
    
    print(f"\nMost Common Themes: {', '.join(summary.most_common_themes)}")
    print(f"Most Common Characters: {', '.join(summary.most_common_characters)}")
    
    # Export metrics
    print("\n📁 Exporting metrics...")
    export_result = metrics_collector.export_metrics()
    
    print("Files created:")
    for file_type, file_path in export_result.items():
        print(f"  {file_type}: {file_path}")
    
    return summary

async def test_single_story_comparison():
    """Test a single story comparison with detailed output"""
    
    print("\n🎯 Single Story Comparison Test")
    print("=" * 60)
    
    # Initialize components
    client = openai.AsyncClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )
    
    rag_generator = RAGStoryGenerator(client)
    
    # Test query
    query = "A brave little mouse who helps a big lion"
    
    print(f"Query: {query}")
    print("\nGenerating stories...")
    
    try:
        # Generate without RAG
        print("\n📝 Generating story WITHOUT RAG...")
        story_without_rag, metrics_without_rag = await rag_generator.generate_story_without_rag(query)
        
        print(f"Generation time: {metrics_without_rag.generation_time:.2f}s")
        print(f"Word count: {metrics_without_rag.word_count}")
        print(f"Character count: {metrics_without_rag.character_count}")
        
        # Generate with RAG
        print("\n📚 Generating story WITH RAG...")
        story_with_rag, metrics_with_rag = await rag_generator.generate_story_with_rag(query)
        
        print(f"Generation time: {metrics_with_rag.generation_time:.2f}s")
        print(f"Word count: {metrics_with_rag.word_count}")
        print(f"Retrieved stories: {metrics_with_rag.retrieved_stories_count}")
        print(f"Retrieved themes: {', '.join(metrics_with_rag.retrieved_themes)}")
        print(f"Retrieved characters: {', '.join(metrics_with_rag.retrieved_characters)}")
        print(f"Similarity scores: {[f'{s:.3f}' for s in metrics_with_rag.similarity_scores]}")
        
        # Analyze quality
        print("\n🔍 Quality Analysis...")
        quality_without_rag = rag_generator.analyze_story_quality(story_without_rag)
        quality_with_rag = rag_generator.analyze_story_quality(story_with_rag)
        
        print("\nWithout RAG Quality:")
        for metric, value in quality_without_rag.items():
            if isinstance(value, float):
                print(f"  {metric}: {value:.3f}")
            else:
                print(f"  {metric}: {value}")
        
        print("\nWith RAG Quality:")
        for metric, value in quality_with_rag.items():
            if isinstance(value, float):
                print(f"  {metric}: {value:.3f}")
            else:
                print(f"  {metric}: {value}")
        
        # Display stories
        print("\n" + "=" * 60)
        print("📝 STORY WITHOUT RAG")
        print("=" * 60)
        print(story_without_rag)
        
        print("\n" + "=" * 60)
        print("📚 STORY WITH RAG")
        print("=" * 60)
        print(story_with_rag)
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Main test function"""
    
    print("🎭 RAG Story Generation Research Test")
    print("This script tests RAG integration with story generation and collects research metrics.")
    print()
    
    # Check if vector store exists
    if not os.path.exists("chroma_db"):
        print("❌ Vector store not found. Please run setup_vector_store.py first.")
        return
    
    # Run tests
    try:
        # Test single comparison
        await test_single_story_comparison()
        
        # Test multiple comparisons
        summary = await test_rag_story_generation()
        
        print("\n✅ All tests completed successfully!")
        print(f"📊 Research data collected for {summary.total_sessions} sessions")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 