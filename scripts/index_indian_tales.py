#!/usr/bin/env python3
"""
Index Indian Tales into Vector Store
Simple script to add Indian tales to the RAG system
"""

import sys
import json
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "app"))

from services.rag.vector_store import VectorStoreManager

def main():
    """Main indexing function"""
    print("🌏 Indexing Indian Tales into Vector Store")
    print("=" * 50)
    
    # Check if processed data exists
    json_path = "rag/indian_tales_processed.json"
    if not os.path.exists(json_path):
        print(f"❌ Processed data not found: {json_path}")
        print("Please run the processing script first:")
        print("python3 scripts/process_indian_tales.py")
        return False
    
    # Load Indian tales
    print("📖 Loading Indian tales...")
    with open(json_path, 'r', encoding='utf-8') as f:
        indian_tales = json.load(f)
    
    print(f"✅ Loaded {len(indian_tales)} Indian tales")
    
    # Initialize vector store manager
    print("\n📦 Initializing Vector Store Manager...")
    manager = VectorStoreManager()
    
    # Index Indian tales
    print("\n🌏 Indexing Indian tales...")
    success = manager.index_data_source(indian_tales, "indian_tales")
    
    if not success:
        print("❌ Failed to index Indian tales")
        return False
    
    # Get collection stats
    print("\n📊 Collection Statistics:")
    stats = manager.get_collection_stats("indian_tales")
    print(f"   Collection: {stats.get('name', 'Unknown')}")
    print(f"   Documents: {stats.get('count', 0)}")
    
    # Test search functionality
    print("\n🔍 Testing Search Functionality...")
    test_queries = [
        "prince and princess",
        "magic and enchantment",
        "family and love",
        "bravery and courage",
        "wisdom and learning"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        results = manager.search_similar_stories(query, "indian_tales", n_results=3)
        
        if results:
            for i, result in enumerate(results, 1):
                title = result["metadata"].get("title", "Unknown")
                distance = result["distance"]
                print(f"     {i}. {title} (distance: {distance:.4f})")
        else:
            print("     No results found")
    
    print("\n✅ Indian Tales Indexing Complete!")
    print("\n🎯 Next Steps:")
    print("   1. Test the RAG system with Indian tales")
    print("   2. Compare story generation with and without Indian tales")
    print("   3. Add more cultural datasets")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 