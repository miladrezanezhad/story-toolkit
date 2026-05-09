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
    """Test Character class functionality"""
    print("\n🎭 Testing Character (v1)...")
    
    # Test creation
    char = Character("Kai", 25, "protagonist")
    assert char.name == "Kai"
    assert char.age == 25
    assert char.role == "protagonist"
    
    # Test traits
    char.add_trait("brave")
    assert "brave" in char.personality_traits
    
    # Test goals
    char.add_goal("Save the kingdom")
    assert "Save the kingdom" in char.goals
    
    # Test skills
    char.add_skill("sword_mastery")
    assert "sword_mastery" in char.skills
    
    # Test relationship
    char.add_relationship("Villain", "enemy", strength=9)
    assert "Villain" in char.relationships
    assert char.relationships["Villain"]["strength"] == 9
    
    # Test arc advancement
    assert char.arc_stage == "initial"
    char.advance_arc()
    assert char.arc_stage == "challenged"
    
    print("   ✅ Character tests passed")
    return True


def test_plot():
    """Test Plot class functionality"""
    print("\n📚 Testing Plot (v1)...")
    
    plot = Plot()
    
    # Test add plot points
    point1 = plot.add_plot_point("Discovery", "Hero finds map", 3, 8)
    point2 = plot.add_plot_point("Climax", "Final battle", 10, 10)
    assert len(plot.plot_points) == 2
    
    # Test connect points
    plot.connect_plot_points(point1.id, point2.id)
    assert point2.id in point1.leads_to
    
    # Test add subplot
    subplot = plot.add_subplot("Love Story", "Romance", ["Hero", "Heroine"])
    assert subplot["title"] == "Love Story"
    assert len(plot.subplots) == 1
    
    # Test timeline
    timeline = plot.get_plot_timeline()
    assert len(timeline) == 2
    
    print("   ✅ Plot tests passed")
    return True


def test_world_builder():
    """Test WorldBuilder class functionality"""
    print("\n🌍 Testing WorldBuilder (v1)...")
    
    world = WorldBuilder()
    
    # Test create world
    world.create_world("Eldoria", "fantasy")
    assert world.name == "Eldoria"
    
    # Test add location
    world.add_location("Crystal City", "Ancient city", "city")
    assert len(world.locations) >= 1
    assert world.locations[0].name == "Crystal City"
    
    # Test add rule
    world.add_rule("magical", "Only pure hearts can use magic")
    assert len(world.rules) >= 1
    
    # Test add faction
    world.add_faction("Shadow Guild", "Secret org", ["control_magic"])
    assert len(world.factions) >= 1
    assert world.factions[0]["name"] == "Shadow Guild"
    
    # Test generate world
    gen_world = world.generate_world("fantasy")
    assert gen_world["type"] == "fantasy"
    assert "key_locations" in gen_world
    
    print("   ✅ WorldBuilder tests passed")
    return True


def test_story_engine():
    """Test StoryEngine class functionality"""
    print("\n📖 Testing StoryEngine (v1)...")
    
    engine = StoryEngine()
    
    # Test create outline
    outline = engine.create_story_outline("fantasy", "courage")
    assert outline is not None
    assert outline["genre"] == "fantasy"
    
    # Test add chapter
    chapter = engine.add_chapter("The Beginning")
    assert chapter["number"] == 1
    
    # Test progress
    progress = engine.get_story_progress()
    assert progress["total_chapters"] == 1
    
    print("   ✅ StoryEngine tests passed")
    return True


def run_all():
    """Run all v1 core tests"""
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
    print(f"\n📊 V1 Core Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)