"""
Story Development Toolkit - Simple Example
===========================================
Quick start example for basic usage.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit import StoryToolkit


def quick_start():
    """Quick start demonstration"""
    print("\n🚀 STORY DEVELOPMENT TOOLKIT - QUICK START")
    print("="*50)
    
    # Create toolkit instance
    toolkit = StoryToolkit()
    
    # Create a simple story
    print("\n1. Creating story...")
    story = toolkit.create_story("adventure", "courage")
    print(f"   ✓ Created {story['metadata']['genre']} story about {story['metadata']['theme']}")
    
    # Add characters
    print("\n2. Adding characters...")
    hero = toolkit.add_character_to_story(story, "Jack Stone", "protagonist")
    hero.add_trait("brave")
    hero.add_trait("determined")
    hero.add_goal("Find the ancient treasure")
    print(f"   ✓ Hero: {hero.name}")
    print(f"   ✓ Traits: {', '.join(hero.personality_traits)}")
    print(f"   ✓ Goals: {', '.join(hero.goals)}")
    
    villain = toolkit.add_character_to_story(story, "Black Morgan", "antagonist")
    villain.add_trait("ruthless")
    villain.add_goal("Steal the treasure for himself")
    print(f"   ✓ Villain: {villain.name}")
    print(f"   ✓ Traits: {', '.join(villain.personality_traits)}")
    
    # Generate dialogue
    print("\n3. Generating dialogue...")
    dialogue = toolkit.dialogue_gen.generate_dialogue(
        "Jack Stone",
        "Black Morgan",
        context="conflict",
        mood="intense"
    )
    for line in dialogue:
        print(f"   {line}")
    
    # Check coherence
    print("\n4. Checking story coherence...")
    sample_data = {
        "characters": [
            {"stage": 0, "personality": "brave"},
            {"stage": 1, "personality": "brave"}
        ],
        "events": [
            {"id": 1, "timestamp": 100},
            {"id": 2, "timestamp": 200}
        ],
        "elements": [
            {"id": "treasure_map", "introduced": True, "resolved": True}
        ]
    }
    report = toolkit.check_story_coherence(sample_data)
    print(f"   ✓ Coherence Score: {report.get('overall_score', 0):.2%}")
    
    # Summary
    print(f"\n{'='*50}")
    print("STORY SUMMARY")
    print(f"{'='*50}")
    print(f"Title: The Quest for Courage")
    print(f"Genre: {story['metadata']['genre']}")
    print(f"Theme: {story['metadata']['theme']}")
    print(f"Characters: {len(story['characters'])}")
    print(f"Coherence: {report.get('overall_score', 0):.2%}")
    
    print(f"\n✅ Quick start completed! Explore more with advanced_example.py")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    quick_start()
