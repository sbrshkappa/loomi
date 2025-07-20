#!/usr/bin/env python3
"""
Vector Store Setup Script
Sets up ChromaDB, indexes Aesop's Fables, and tests search functionality
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "app"))

from services.rag.vector_store import VectorStoreManager

def main():
    """Main setup function"""
    print("🚀 Setting up Vector Store for RAG System")
    print("=" * 50)
    
    # Initialize vector store manager
    print("📦 Initializing Vector Store Manager...")
    manager = VectorStoreManager()
    
    # Check if processed data exists
    json_path = "rag/aesop_fables_processed.json"
    if not os.path.exists(json_path):
        print(f"❌ Processed data not found: {json_path}")
        print("Please run the processing script first:")
        print("python3 scripts/process_aesop_fables.py")
        return False
    
    # Index Aesop's Fables
    print("\n📚 Indexing Aesop's Fables...")
    success = manager.index_aesop_fables()
    
    if not success:
        print("❌ Failed to index Aesop's Fables")
        return False
    
    # Get collection stats
    print("\n📊 Collection Statistics:")
    stats = manager.get_collection_stats()
    print(f"   Collection: {stats.get('name', 'Unknown')}")
    print(f"   Documents: {stats.get('count', 0)}")
    
    # Test search functionality
    print("\n🔍 Testing Search Functionality...")
    test_queries = [
        "brave lion",
        "clever fox",
        "honesty and truth",
        "friendship and loyalty",
        "hard work pays off"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        results = manager.search_similar_stories(query, n_results=3)
        
        if results:
            for i, result in enumerate(results, 1):
                title = result["metadata"].get("title", "Unknown")
                distance = result["distance"]
                print(f"     {i}. {title} (distance: {distance:.4f})")
        else:
            print("     No results found")
    
    print("\n✅ Vector Store Setup Complete!")
    print("\n📁 Files created:")
    print("   - ./chroma_db/ (vector database)")
    print("   - ./chroma_db/aesop_fables/ (Aesop's Fables collection)")
    
    print("\n🎯 Next Steps:")
    print("   1. Test the RAG retriever integration")
    print("   2. Add animated movies dataset")
    print("   3. Add animal facts dataset")
    print("   4. Integrate with story generation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 