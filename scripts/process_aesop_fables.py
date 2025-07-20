#!/usr/bin/env python3
"""
Script to process Aesop's Fables from Project Gutenberg text into structured JSON.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag.document_processor import AesopProcessor
import json


def main():
    """Process Aesop's Fables and generate structured dataset."""
    
    # File paths
    input_file = "rag/aesop_fables.txt"
    output_file = "rag/aesop_fables_processed.json"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        print("Please download the Aesop's Fables text file to the 'rag' directory.")
        return
    
    # Create processor and process file
    processor = AesopProcessor()
    
    try:
        print("🚀 Starting Aesop's Fables processing...")
        fables = processor.process_file(input_file)
        
        if not fables:
            print("❌ No fables were processed successfully!")
            return
        
        # Export to JSON
        processor.export_json(output_file)
        
        # Print statistics
        stats = processor.get_statistics()
        print("\n📊 Processing Statistics:")
        print(f"   Total fables: {stats['total_fables']}")
        print(f"   Total words: {stats['total_words']:,}")
        print(f"   Average words per fable: {stats['average_words']}")
        print(f"   Unique themes: {stats['unique_themes']}")
        print(f"   Unique characters: {stats['unique_characters']}")
        
        print(f"\n📈 Age Group Distribution:")
        for age_group, count in stats['age_group_distribution'].items():
            print(f"   {age_group}: {count} fables")
        
        print(f"\n📊 Difficulty Distribution:")
        for difficulty, count in stats['difficulty_distribution'].items():
            print(f"   {difficulty}: {count} fables")
        
        print(f"\n🎭 Most Common Characters:")
        for character, count in stats['most_common_characters'][:5]:
            print(f"   {character}: {count} appearances")
        
        print(f"\n🎯 Most Common Themes:")
        for theme, count in stats['most_common_themes'][:5]:
            print(f"   {theme}: {count} occurrences")
        
        print(f"\n✅ Successfully processed {len(fables)} fables!")
        print(f"📁 Output saved to: {output_file}")
        
        # Show sample fable
        if fables:
            sample = fables[0]
            print(f"\n📖 Sample Fable:")
            print(f"   Title: {sample.title}")
            print(f"   Characters: {', '.join(sample.characters)}")
            print(f"   Themes: {', '.join(sample.themes)}")
            print(f"   Moral: {sample.moral}")
            print(f"   Age Group: {sample.age_group}")
            print(f"   Difficulty: {sample.difficulty}")
        
    except Exception as e:
        print(f"❌ Error processing fables: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 