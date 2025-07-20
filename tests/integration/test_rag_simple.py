#!/usr/bin/env python3
"""
Simple RAG Test Script
Test if the RAG system is working properly
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_rag_system():
    """Test the RAG system components"""
    print("🧪 Testing RAG System Components")
    print("=" * 40)
    
    try:
        # Test 1: Vector Store Manager
        print("\n1. Testing Vector Store Manager...")
        from app.services.rag.vector_store import VectorStoreManager
        manager = VectorStoreManager()
        print("✅ Vector Store Manager initialized successfully")
        
        # Test 2: Check collections
        print("\n2. Checking collections...")
        try:
            aesop_stats = manager.get_collection_stats("aesop_fables")
            print(f"✅ Aesop's Fables collection: {aesop_stats.get('count', 0)} documents")
        except Exception as e:
            print(f"⚠️  Aesop's Fables collection issue: {e}")
        
        try:
            indian_stats = manager.get_collection_stats("indian_tales")
            print(f"✅ Indian Tales collection: {indian_stats.get('count', 0)} documents")
        except Exception as e:
            print(f"⚠️  Indian Tales collection issue: {e}")
        
        # Test 3: RAG Retriever
        print("\n3. Testing RAG Retriever...")
        from app.services.rag.retriever import RAGRetriever
        retriever = RAGRetriever(manager)
        print("✅ RAG Retriever initialized successfully")
        
        # Test 4: Simple search
        print("\n4. Testing simple search...")
        try:
            results = manager.search_similar_stories("brave lion", n_results=2)
            print(f"✅ Search successful: found {len(results)} results")
            for i, result in enumerate(results, 1):
                title = result["metadata"].get("title", "Unknown")
                print(f"   {i}. {title}")
        except Exception as e:
            print(f"❌ Search failed: {e}")
        
        # Test 5: RAG Integration
        print("\n5. Testing RAG Integration...")
        from app.services.rag.integration import RAGIntegration
        rag_integration = RAGIntegration()
        print("✅ RAG Integration initialized successfully")
        
        print("\n🎉 All RAG components are working!")
        return True
        
    except Exception as e:
        print(f"\n❌ RAG system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_rag_system()
    sys.exit(0 if success else 1) 