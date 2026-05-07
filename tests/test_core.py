"""
Tests for core modules.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit.core.story_engine import StoryEngine
from story_toolkit.core.character import Character
from story_toolkit.core.plot import Plot, PlotPoint
from story_toolkit.core.world_builder import WorldBuilder


def test_story_engine():
    """Test StoryEngine functionality"""
    print("\nTesting StoryEngine...")
    
    engine = StoryEngine()
    
    # Test story outline creation
    outline = engine.create_story_outline("fantasy", "courage")
    assert outline["genre"] == "fantasy"
    assert outline["theme"] == "courage"
    assert "structure" in outline
    print("  ✓ Story outline creation")
    
    # Test chapter management
    chapter = engine.add_chapter("The Beginning")
    assert chapter["number"] == 1
    assert chapter["title"] == "The Beginning"
    print("  ✓ Chapter management")
    
    # Test progress tracking
    progress = engine.get_story_progress()
    assert progress["total_chapters"] == 1
    print("  ✓ Progress tracking")
    
    # Test validation
    issues = engine.validate_structure()
    assert len(issues) > 0  # Should have issues (no title, characters)
    print("  ✓ Structure validation")
    
    print("✅ StoryEngine tests passed!")


def test_character():
    """Test Character functionality"""
    print("\nTesting Character...")
    
    # Test creation
    char = Character("Test Hero", 25, "protagonist")
    assert char.name == "Test Hero"
    assert char.age == 25
    assert char.role == "protagonist"
    print("  ✓ Character creation")
    
    # Test trait management
    char.add_trait("brave")
    assert "brave" in char.personality_traits
    char.add_trait("brave")  # Duplicate should not add
    assert len(char.personality_traits) == 1
    print("  ✓ Trait management")
    
    # Test goals
    char.add_goal("Save the world")
    assert len(char.goals) == 1
    print("  ✓ Goal management")
    
    # Test skills
    char.add_skill("combat")
    assert "combat" in char.skills
    print("  ✓ Skill management")
    
    # Test weaknesses
    char.add_weakness("overconfidence")
    assert "overconfidence" in char.weaknesses
    print("  ✓ Weakness management")
    
    # Test fears
    char.add_fear("darkness")
    assert "darkness" in char.fears
    print("  ✓ Fear management")
    
    # Test relationships
    char.add_relationship("Villain", "enemy", 8)
    assert "Villain" in char.relationships
    assert char.relationships["Villain"]["strength"] == 8
    print("  ✓ Relationship management")
    
    # Test arc advancement
    assert char.arc_stage == "initial"
    char.advance_arc()
    assert char.arc_stage == "challenged"
    print("  ✓ Arc advancement")
    
    # Test character arc
    arc = char.get_character_arc()
    assert arc["name"] == "Test Hero"
    assert arc["role"] == "protagonist"
    print("  ✓ Character arc retrieval")
    
    # Test to_dict
    char_dict = char.to_dict()
    assert char_dict["name"] == "Test Hero"
    print("  ✓ Dictionary conversion")
    
    print("✅ Character tests passed!")


def test_plot():
    """Test Plot functionality"""
    print("\nTesting Plot...")
    
    plot = Plot()
    
    # Test plot point creation
    point = plot.add_plot_point("The Hook", "Story begins", 1, 8)
    assert point.title == "The Hook"
    assert point.importance == 8
    print("  ✓ Plot point creation")
    
    # Test multiple points
    point2 = plot.add_plot_point("The Climax", "Final battle", 10, 10)
    assert len(plot.plot_points) == 2
    print("  ✓ Multiple plot points")
    
    # Test point connection
    plot.connect_plot_points(point.id, point2.id)
    assert point2.id in point.leads_to
    print("  ✓ Plot point connection")
    
    # Test subplot creation
    subplot = plot.add_subplot("Love Story", "Romance subplot", ["Hero", "Heroine"])
    assert subplot["title"] == "Love Story"
    assert len(plot.subplots) == 1
    print("  ✓ Subplot creation")
    
    # Test plot summary
    summary = plot.get_plot_summary()
    assert summary["total_points"] == 2
    assert summary["subplots"] == 1
    print("  ✓ Plot summary")
    
    # Test timeline
    timeline = plot.get_plot_timeline()
    assert len(timeline) == 2
    print("  ✓ Plot timeline")
    
    print("✅ Plot tests passed!")


def test_world_builder():
    """Test WorldBuilder functionality"""
    print("\nTesting WorldBuilder...")
    
    world = WorldBuilder()
    
    # Test world creation
    world_data = world.create_world("Test World", "fantasy")
    assert world.name == "Test World"
    assert world.type == "fantasy"
    print("  ✓ World creation")
    
    # Test location creation
    location = world.add_location("Test City", "A test city", "city")
    assert location.name == "Test City"
    assert len(world.locations) == 1
    print("  ✓ Location creation")
    
    # Test location connection
    location2 = world.add_location("Test Forest", "A test forest", "forest")
    world.connect_locations("Test City", "Test Forest")
    assert "Test Forest" in location.connected_locations
    print("  ✓ Location connection")
    
    # Test rules
    world.add_rule("physical", "Gravity exists")
    assert "Gravity exists" in world.rules["physical"]
    print("  ✓ Rule addition")
    
    # Test culture creation
    culture = world.add_culture("Test Culture", "A test culture", ["custom1"])
    assert culture["name"] == "Test Culture"
    assert len(world.cultures) == 1
    print("  ✓ Culture creation")
    
    # Test faction creation
    faction = world.add_faction("Test Faction", "A test faction", ["goal1"])
    assert faction["name"] == "Test Faction"
    assert len(world.factions) == 1
    print("  ✓ Faction creation")
    
    # Test world generation
    gen_world = world.generate_world("fantasy")
    assert gen_world["type"] == "fantasy"
    assert "key_locations" in gen_world
    print("  ✓ World generation")
    
    # Test summary
    summary = world.get_world_summary()
    assert summary["total_locations"] == 2
    print("  ✓ World summary")
    
    print("✅ WorldBuilder tests passed!")


if __name__ == "__main__":
    print("\n🧪 STORY TOOLKIT - CORE TESTS")
    print("="*40)
    
    test_story_engine()
    test_character()
    test_plot()
    test_world_builder()
    
    print(f"\n{'='*40}")
    print("✅ All core tests passed!")
    print(f"{'='*40}\n")
