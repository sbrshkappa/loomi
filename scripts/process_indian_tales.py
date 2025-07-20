#!/usr/bin/env python3
"""
Script to process Indian Fairy Tales from Project Gutenberg text into structured JSON.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag.document_processor import ChildrensTaleTextProcessor
import json


def main():
    """Process Indian Fairy Tales and generate structured dataset."""
    
    # File paths
    input_file = "rag/indian_tales_gutenberg.txt"
    output_file = "rag/indian_tales_processed.json"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        print("Please ensure the Indian tales Gutenberg file is in the 'rag' directory.")
        return
    
    # Create processor for Indian tales
    processor = ChildrensTaleTextProcessor(tale_type="indian")
    
    try:
        # Process the file
        tales = processor.process_file(input_file)
        
        if not tales:
            print("No tales were processed successfully.")
            return
        
        # Export to JSON
        processor.export_json(output_file)
        
        # Show statistics
        print("\n📊 Processing Statistics:")
        print(f"   Total tales processed: {len(tales)}")
        
        # Age group distribution
        age_groups = {}
        for tale in tales:
            age_groups[tale.age_group] = age_groups.get(tale.age_group, 0) + 1
        
        print("   Age group distribution:")
        for age_group, count in sorted(age_groups.items()):
            print(f"     {age_group}: {count} tales")
        
        # Theme distribution
        all_themes = []
        for tale in tales:
            all_themes.extend(tale.themes)
        
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        print("   Top themes:")
        for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"     {theme}: {count} tales")
        
        # Character distribution
        all_characters = []
        for tale in tales:
            all_characters.extend(tale.characters)
        
        character_counts = {}
        for character in all_characters:
            character_counts[character] = character_counts.get(character, 0) + 1
        
        print("   Top characters:")
        for character, count in sorted(character_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"     {character}: {count} tales")
        
        # Word count statistics
        word_counts = [tale.word_count for tale in tales]
        avg_words = sum(word_counts) / len(word_counts)
        print(f"   Average word count: {avg_words:.1f} words")
        print(f"   Shortest tale: {min(word_counts)} words")
        print(f"   Longest tale: {max(word_counts)} words")
        
        print(f"\n✅ Successfully processed Indian Fairy Tales!")
        print(f"📁 Output file: {output_file}")
        print("\n🎯 Next Steps:")
        print("1. Run the vector store setup to index the tales:")
        print("   python scripts/setup_vector_store.py")
        print("2. Test the RAG system with Indian tales:")
        print("   python tests/integration/test_rag_toggle.py")
        
    except Exception as e:
        print(f"❌ Error processing Indian tales: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 