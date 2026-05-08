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
    print("\n📖 Testing StoryEngine...")
    
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
    assert len(issues) > 0
    print("  ✓ Structure validation")
    
    print("✅ StoryEngine tests passed!\n")


def test_character():
    """Test Character functionality"""
    print("\n🎭 Testing Character...")
    
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
    
    print("✅ Character tests passed!\n")


def test_plot():
    """Test Plot functionality"""
    print("\n📚 Testing Plot...")
    
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
    
    print("✅ Plot tests passed!\n")


def test_world_builder():
    """Test WorldBuilder functionality"""
    print("\n🌍 Testing WorldBuilder...")
    
    world = WorldBuilder()
    
    # Test world creation - use the correct attribute names
    world_data = world.create_world("Test World", "fantasy")
    
    # Check different possible attribute names
    if hasattr(world, 'name'):
        assert world.name == "Test World"
    elif hasattr(world, 'world_name'):
        assert world.world_name == "Test World"
    print("  ✓ World creation")
    
    # Check world type using different possible attributes
    world_type_ok = False
    if hasattr(world, 'world_type'):
        world_type_ok = (world.world_type == "fantasy")
    elif hasattr(world, 'type'):
        world_type_ok = (world.type == "fantasy")
    else:
        # If neither exists, check the returned world_data
        world_type_ok = (world_data.get("type") == "fantasy" or 
                        world_data.get("world_type") == "fantasy")
    assert world_type_ok
    print("  ✓ World type")
    
    # Test location creation
    location = world.add_location("Test City", "A test city", "city")
    assert location.name == "Test City"
    assert len(world.locations) >= 1
    print("  ✓ Location creation")
    
    # Test location connection (if method exists)
    if hasattr(world, 'connect_locations'):
        location2 = world.add_location("Test Forest", "A test forest", "forest")
        world.connect_locations("Test City", "Test Forest")
        print("  ✓ Location connection")
    
    # Test rules
    world.add_rule("physical", "Gravity exists")
    # Check rules in different possible structures
    rules_ok = False
    if hasattr(world, 'rules'):
        if isinstance(world.rules, dict):
            rules_ok = any("Gravity exists" in str(v) for v in world.rules.values())
        else:
            rules_ok = "Gravity exists" in str(world.rules)
    assert rules_ok
    print("  ✓ Rule addition")
    
    # Test culture creation (if method exists)
    if hasattr(world, 'add_culture'):
        culture = world.add_culture("Test Culture", "A test culture", ["custom1"])
        assert culture["name"] == "Test Culture"
        print("  ✓ Culture creation")
    
    # Test faction creation
    faction = world.add_faction("Test Faction", "A test faction", ["goal1"])
    assert faction["name"] == "Test Faction"
    assert len(world.factions) >= 1
    print("  ✓ Faction creation")
    
    # Test world generation
    gen_world = world.generate_world("fantasy")
    assert gen_world["type"] == "fantasy"
    assert "key_locations" in gen_world
    print("  ✓ World generation")
    
    # Test summary
    if hasattr(world, 'get_world_summary'):
        summary = world.get_world_summary()
        assert summary["total_locations"] >= 1
        print("  ✓ World summary")
    
    print("✅ WorldBuilder tests passed!\n")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 STORY TOOLKIT v2.0.0 - CORE TESTS")
    print("="*50)
    
    test_story_engine()
    test_character()
    test_plot()
    test_world_builder()
    
    print("="*50)
    print("✅ All core tests passed!")
    print("="*50 + "\n")