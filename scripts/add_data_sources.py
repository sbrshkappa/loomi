#!/usr/bin/env python3
"""
Add New Data Sources to RAG System
Helps add animated movies, animal facts, and other content to the vector store
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.rag.vector_store import VectorStoreManager

# Sample data sources
ANIMATED_MOVIES_DATA = [
    {
        "id": "movie_001",
        "title": "The Lion King",
        "content": "A young lion prince named Simba learns about responsibility and leadership after his father's death. He must overcome his fears and take his rightful place as king of the Pride Lands.",
        "themes": ["responsibility", "leadership", "family", "courage", "redemption"],
        "characters": ["lion", "hyena", "meerkat", "warthog", "bird"],
        "age_group": "5-12",
        "difficulty": "medium",
        "moral": "True leadership comes from responsibility and courage.",
        "source": "disney_animated"
    },
    {
        "id": "movie_002", 
        "title": "Finding Nemo",
        "content": "A clownfish named Marlin embarks on a journey across the ocean to find his son Nemo, who was captured by divers. Along the way, he learns to let go of his fears and trust others.",
        "themes": ["family", "trust", "friendship", "perseverance", "letting go"],
        "characters": ["fish", "shark", "turtle", "seagull", "octopus"],
        "age_group": "3-10",
        "difficulty": "easy",
        "moral": "Love and determination can overcome any obstacle.",
        "source": "pixar_animated"
    }
]

ANIMAL_FACTS_DATA = [
    {
        "id": "animal_001",
        "title": "The Curious Elephant",
        "content": "Elephants are the largest land animals on Earth. They have excellent memories and strong family bonds. Baby elephants stay with their mothers for many years, learning important life skills.",
        "themes": ["family", "learning", "memory", "strength", "wisdom"],
        "characters": ["elephant", "baby elephant", "herd"],
        "age_group": "3-8",
        "difficulty": "easy", 
        "moral": "Family bonds and learning are important for growth.",
        "source": "animal_facts"
    },
    {
        "id": "animal_002",
        "title": "The Clever Dolphin",
        "content": "Dolphins are highly intelligent marine mammals. They communicate with clicks and whistles, work together to catch fish, and even help injured dolphins in their pod.",
        "themes": ["intelligence", "cooperation", "communication", "helping others"],
        "characters": ["dolphin", "fish", "pod"],
        "age_group": "5-10",
        "difficulty": "medium",
        "moral": "Working together and helping others makes everyone stronger.",
        "source": "animal_facts"
    }
]

def add_animated_movies():
    """Add animated movies data to the vector store"""
    print("🎬 Adding Animated Movies Data...")
    
    # Save to JSON file
    output_file = "rag/animated_movies_processed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ANIMATED_MOVIES_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(ANIMATED_MOVIES_DATA)} animated movies to {output_file}")
    return ANIMATED_MOVIES_DATA

def add_animal_facts():
    """Add animal facts data to the vector store"""
    print("🦁 Adding Animal Facts Data...")
    
    # Save to JSON file
    output_file = "rag/animal_facts_processed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ANIMAL_FACTS_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(ANIMAL_FACTS_DATA)} animal facts to {output_file}")
    return ANIMAL_FACTS_DATA

def index_new_data_sources():
    """Index new data sources into the vector store"""
    print("📚 Indexing New Data Sources...")
    
    # Initialize vector store manager
    manager = VectorStoreManager()
    
    # Index animated movies
    print("\n🎬 Indexing Animated Movies...")
    animated_movies = add_animated_movies()
    success = manager.index_data_source(animated_movies, "animated_movies")
    
    if success:
        print("✅ Animated movies indexed successfully!")
    else:
        print("❌ Failed to index animated movies")
    
    # Index animal facts
    print("\n🦁 Indexing Animal Facts...")
    animal_facts = add_animal_facts()
    success = manager.index_data_source(animal_facts, "animal_facts")
    
    if success:
        print("✅ Animal facts indexed successfully!")
    else:
        print("❌ Failed to index animal facts")
    
    # Show collection stats
    print("\n📊 Collection Statistics:")
    for collection_name in ["aesop_fables", "animated_movies", "animal_facts"]:
        stats = manager.get_collection_stats(collection_name)
        print(f"   {collection_name}: {stats.get('count', 0)} documents")

def show_embedding_strategy():
    """Show embedding generation strategy"""
    print("\n🔄 Embedding Generation Strategy")
    print("=" * 50)
    
    print("📅 When to Regenerate Embeddings:")
    print("✅ New data sources added")
    print("✅ Model updates (better embedding model)")
    print("✅ Data quality improvements")
    print("✅ Performance issues detected")
    print()
    print("❌ Don't regenerate for:")
    print("❌ Minor content updates")
    print("❌ Metadata changes only")
    print("❌ Frequent small additions")
    
    print("\n🛠️ Commands:")
    print("   # Add new data sources")
    print("   python scripts/add_data_sources.py")
    print()
    print("   # Regenerate all embeddings")
    print("   python scripts/setup_vector_store.py --force-reindex")
    print()
    print("   # Test search quality")
    print("   python tests/integration/test_rag_toggle.py")

def main():
    """Main function"""
    print("🚀 Adding New Data Sources to RAG System")
    print("=" * 60)
    
    # Check if vector store exists
    if not os.path.exists("chroma_db"):
        print("❌ Vector store not found. Please run setup_vector_store.py first.")
        return
    
    # Add new data sources
    index_new_data_sources()
    
    # Show strategy
    show_embedding_strategy()
    
    print("\n✅ Data sources added successfully!")
    print("\n🎯 Next Steps:")
    print("1. Test the new data sources with story generation")
    print("2. Monitor search quality and relevance")
    print("3. Add more data sources as needed")
    print("4. Consider fine-tuning similarity thresholds")

if __name__ == "__main__":
    main() 