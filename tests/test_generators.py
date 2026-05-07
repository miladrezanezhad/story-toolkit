"""
Tests for generator modules.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit.generators.character_generator import CharacterGenerator
from story_toolkit.generators.plot_generator import PlotGenerator
from story_toolkit.generators.dialogue_generator import DialogueGenerator


def test_character_generator():
    """Test CharacterGenerator functionality"""
    print("\nTesting CharacterGenerator...")
    
    gen = CharacterGenerator()
    
    # Test single character generation
    char = gen.generate_character("protagonist", complexity=4)
    assert char is not None
    assert char.name != ""
    assert char.role == "protagonist"
    assert len(char.personality_traits) > 0
    assert len(char.goals) > 0
    assert len(char.skills) > 0
    assert len(char.weaknesses) > 0
    assert char.background != ""
    print("  ✓ Single character generation")
    
    # Test ensemble generation
    ensemble = gen.generate_ensemble(4)
    assert len(ensemble) == 4
    roles = [c.role for c in ensemble]
    assert "protagonist" in roles
    assert "antagonist" in roles
    print("  ✓ Ensemble generation")
    
    # Test character with backstory
    char2 = gen.generate_with_backstory("mentor", "redemption")
    assert char2 is not None
    assert char2.background != ""
    print("  ✓ Character with backstory")
    
    print("✅ CharacterGenerator tests passed!")


def test_plot_generator():
    """Test PlotGenerator functionality"""
    print("\nTesting PlotGenerator...")
    
    gen = PlotGenerator()
    
    # Test plot generation for different genres
    genres = ["mystery", "fantasy", "romance", "adventure", "sci_fi"]
    
    for genre in genres:
        plot = gen.generate_plot(genre, complexity=3)
        
        assert plot["genre"] == genre
        assert "main_plot" in plot
        assert len(plot["main_plot"]) > 0
        assert "subplots" in plot
        assert "twists" in plot
        assert "pacing" in plot
        assert "estimated_length" in plot
        
        # Check estimated length
        assert plot["estimated_length"]["estimated_chapters"] > 0
        assert plot["estimated_length"]["estimated_words"] > 0
        
        print(f"  ✓ {genre} plot generation")
    
    # Test twist suggestion
    twist = gen.suggest_twist([])
    assert twist is not None
    assert len(twist) > 0
    print("  ✓ Twist suggestion")
    
    print("✅ PlotGenerator tests passed!")


def test_dialogue_generator():
    """Test DialogueGenerator functionality"""
    print("\nTesting DialogueGenerator...")
    
    gen = DialogueGenerator()
    
    # Test dialogue generation
    dialogue = gen.generate_dialogue(
        "Hero", "Villain",
        context="conflict",
        mood="tense"
    )
    assert len(dialogue) > 0
    assert all(isinstance(line, str) for line in dialogue)
    assert "Hero" in dialogue[0]
    print("  ✓ Dialogue generation")
    
    # Test different contexts
    contexts = ["conflict", "revelation", "emotional", "romantic"]
    for context in contexts:
        dialogue = gen.generate_dialogue("Char1", "Char2", context=context)
        assert len(dialogue) > 0
        print(f"  ✓ {context} context dialogue")
    
    # Test scene creation
    characters = [
        {"name": "Hero", "role": "protagonist"},
        {"name": "Villain", "role": "antagonist"}
    ]
    
    scene = gen.create_conversation_scene(characters, "confrontation")
    assert "setting" in scene
    assert "atmosphere" in scene
    assert "dialogue" in scene
    assert scene["dialogue"] is not None
    print("  ✓ Scene creation")
    
    # Test monologue generation
    monologue = gen.generate_monologue("Hero", "destiny", "reflective")
    assert len(monologue) > 0
    print("  ✓ Monologue generation")
    
    print("✅ DialogueGenerator tests passed!")


if __name__ == "__main__":
    print("\n🧪 STORY TOOLKIT - GENERATOR TESTS")
    print("="*40)
    
    test_character_generator()
    test_plot_generator()
    test_dialogue_generator()
    
    print(f"\n{'='*40}")
    print("✅ All generator tests passed!")
    print(f"{'='*40}\n")
