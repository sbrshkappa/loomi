#!/usr/bin/env python3
"""
Script to validate the processed Aesop's Fables dataset.
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def validate_dataset(file_path: str):
    """Validate the processed dataset."""
    
    print(f"🔍 Validating dataset: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        fables = json.load(f)
    
    print(f"📊 Total fables loaded: {len(fables)}")
    
    # Validation checks
    issues = []
    stats = {
        "total_fables": len(fables),
        "fables_with_morals": 0,
        "fables_with_themes": 0,
        "fables_with_characters": 0,
        "fables_with_content": 0,
        "avg_word_count": 0,
        "age_groups": {},
        "difficulties": {},
        "themes": {},
        "characters": {}
    }
    
    total_words = 0
    
    for i, fable in enumerate(fables):
        # Check required fields
        if not fable.get("id"):
            issues.append(f"Fable {i+1}: Missing ID")
        
        if not fable.get("title"):
            issues.append(f"Fable {i+1}: Missing title")
        
        if not fable.get("content"):
            issues.append(f"Fable {i+1}: Missing content")
        else:
            stats["fables_with_content"] += 1
            word_count = fable.get("word_count", 0)
            total_words += word_count
        
        if fable.get("moral"):
            stats["fables_with_morals"] += 1
        
        if fable.get("themes") and len(fable["themes"]) > 0:
            stats["fables_with_themes"] += 1
            for theme in fable["themes"]:
                stats["themes"][theme] = stats["themes"].get(theme, 0) + 1
        
        if fable.get("characters") and len(fable["characters"]) > 0:
            stats["fables_with_characters"] += 1
            for character in fable["characters"]:
                stats["characters"][character] = stats["characters"].get(character, 0) + 1
        
        # Track age groups and difficulties
        age_group = fable.get("age_group", "unknown")
        stats["age_groups"][age_group] = stats["age_groups"].get(age_group, 0) + 1
        
        difficulty = fable.get("difficulty", "unknown")
        stats["difficulties"][difficulty] = stats["difficulties"].get(difficulty, 0) + 1
    
    # Calculate averages
    if stats["total_fables"] > 0:
        stats["avg_word_count"] = round(total_words / stats["total_fables"], 1)
    
    # Print results
    print(f"\n✅ Validation Results:")
    print(f"   Total fables: {stats['total_fables']}")
    print(f"   Fables with content: {stats['fables_with_content']}")
    print(f"   Fables with morals: {stats['fables_with_morals']}")
    print(f"   Fables with themes: {stats['fables_with_themes']}")
    print(f"   Fables with characters: {stats['fables_with_characters']}")
    print(f"   Average word count: {stats['avg_word_count']}")
    
    print(f"\n📈 Age Group Distribution:")
    for age_group, count in sorted(stats["age_groups"].items()):
        percentage = (count / stats["total_fables"]) * 100
        print(f"   {age_group}: {count} ({percentage:.1f}%)")
    
    print(f"\n📊 Difficulty Distribution:")
    for difficulty, count in sorted(stats["difficulties"].items()):
        percentage = (count / stats["total_fables"]) * 100
        print(f"   {difficulty}: {count} ({percentage:.1f}%)")
    
    print(f"\n🎯 Top 10 Themes:")
    sorted_themes = sorted(stats["themes"].items(), key=lambda x: x[1], reverse=True)
    for theme, count in sorted_themes[:10]:
        print(f"   {theme}: {count}")
    
    print(f"\n🎭 Top 10 Characters:")
    sorted_characters = sorted(stats["characters"].items(), key=lambda x: x[1], reverse=True)
    for character, count in sorted_characters[:10]:
        print(f"   {character}: {count}")
    
    if issues:
        print(f"\n⚠️  Issues Found:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print(f"\n✅ No validation issues found!")
        return True

def show_sample_fables(file_path: str, num_samples: int = 3):
    """Show sample fables from the dataset."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        fables = json.load(f)
    
    print(f"\n📖 Sample Fables:")
    
    for i in range(min(num_samples, len(fables))):
        fable = fables[i]
        print(f"\n--- Sample {i+1}: {fable['title']} ---")
        print(f"ID: {fable['id']}")
        print(f"Characters: {', '.join(fable['characters']) if fable['characters'] else 'None'}")
        print(f"Themes: {', '.join(fable['themes']) if fable['themes'] else 'None'}")
        print(f"Moral: {fable['moral']}")
        print(f"Age Group: {fable['age_group']}")
        print(f"Difficulty: {fable['difficulty']}")
        print(f"Word Count: {fable['word_count']}")
        
        # Show first 100 characters of content
        content_preview = fable['content'][:100] + "..." if len(fable['content']) > 100 else fable['content']
        print(f"Content Preview: {content_preview}")

def main():
    """Main validation function."""
    
    file_path = "rag/aesop_fables_processed.json"
    
    if not os.path.exists(file_path):
        print(f"❌ Dataset file not found: {file_path}")
        print("Please run the processing script first: python3 scripts/process_aesop_fables.py")
        return
    
    # Validate the dataset
    is_valid = validate_dataset(file_path)
    
    # Show sample fables
    show_sample_fables(file_path)
    
    if is_valid:
        print(f"\n🎉 Dataset validation completed successfully!")
        print(f"✅ Ready for RAG integration!")
    else:
        print(f"\n❌ Dataset has validation issues that should be addressed.")

if __name__ == "__main__":
    main() 