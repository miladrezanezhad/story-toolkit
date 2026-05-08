"""
Tests for v1.0.0 - Core modules (Character, Plot, WorldBuilder, StoryEngine)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit.core.character import Character
from story_toolkit.core.plot import Plot
from story_toolkit.core.world_builder import WorldBuilder
from story_toolkit.core.story_engine import StoryEngine


def test_character():
    print("\n🎭 Testing Character (v1)...")
    
    char = Character("Kai", 25, "protagonist")
    char.add_trait("brave")
    char.add_goal("Save the kingdom")
    char.add_skill("sword_mastery")
    char.add_relationship("Villain", "enemy", strength=9)
    
    assert char.name == "Kai"
    assert "brave" in char.personality_traits
    assert "Save the kingdom" in char.goals
    assert "sword_mastery" in char.skills
    assert "Villain" in char.relationships
    
    print("   ✅ Character tests passed")
    return True


def test_plot():
    print("\n📚 Testing Plot (v1)...")
    
    plot = Plot()
    point1 = plot.add_plot_point("Discovery", "Hero finds map", 3, 8)
    point2 = plot.add_plot_point("Climax", "Final battle", 10, 10)
    plot.connect_plot_points(point1.id, point2.id)
    
    assert len(plot.plot_points) == 2
    assert point2.id in point1.leads_to
    
    print("   ✅ Plot tests passed")
    return True


def test_world_builder():
    print("\n🌍 Testing WorldBuilder (v1)...")
    
    world = WorldBuilder()
    world.create_world("Eldoria", "fantasy")
    world.add_location("Crystal City", "Ancient city", "city")
    world.add_rule("magical", "Only pure hearts can use magic")
    world.add_faction("Shadow Guild", "Secret org", ["control_magic"])
    
    assert world.name == "Eldoria"
    assert len(world.locations) >= 1
    assert len(world.factions) >= 1
    
    print("   ✅ WorldBuilder tests passed")
    return True


def test_story_engine():
    print("\n📖 Testing StoryEngine (v1)...")
    
    engine = StoryEngine()
    outline = engine.create_story_outline("fantasy", "courage")
    chapter = engine.add_chapter("The Beginning")
    
    assert outline is not None
    assert chapter["number"] == 1
    
    print("   ✅ StoryEngine tests passed")
    return True


def run_all():
    print("\n" + "="*60)
    print("🧪 V1.0.0 - CORE TESTS")
    print("="*60)
    
    results = []
    results.append(("Character", test_character()))
    results.append(("Plot", test_plot()))
    results.append(("WorldBuilder", test_world_builder()))
    results.append(("StoryEngine", test_story_engine()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V1 Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    run_all()
