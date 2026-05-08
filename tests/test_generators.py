"""
Tests for generator modules including new LLM support.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit.generators.character_generator import CharacterGenerator
from story_toolkit.generators.plot_generator import PlotGenerator
from story_toolkit.generators.dialogue_generator import DialogueGenerator
from story_toolkit.llm import LLMFactory, LLMProvider


def test_character_generator():
    """Test CharacterGenerator functionality"""
    print("\n👤 Testing CharacterGenerator...")
    
    gen = CharacterGenerator()
    
    # Test single character generation
    char = gen.generate_character("protagonist", complexity=4)
    assert char is not None
    assert char.name != ""
    assert char.role == "protagonist"
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
    
    print("✅ CharacterGenerator tests passed!\n")


def test_plot_generator():
    """Test PlotGenerator functionality"""
    print("\n📖 Testing PlotGenerator...")
    
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
        
        print(f"  ✓ {genre} plot generation")
    
    # Test twist suggestion
    twist = gen.suggest_twist([])
    assert twist is not None
    assert len(twist) > 0
    print("  ✓ Twist suggestion")
    
    print("✅ PlotGenerator tests passed!\n")


def test_dialogue_generator_without_llm():
    """Test DialogueGenerator without LLM (legacy mode)"""
    print("\n💬 Testing DialogueGenerator (Legacy Mode)...")
    
    gen = DialogueGenerator()  # No LLM
    
    # Test basic dialogue generation
    dialogue = gen.generate_dialogue(
        "Hero", "Villain",
        context="conflict",
        num_lines=3
    )
    assert len(dialogue) > 0
    assert all(isinstance(line, str) for line in dialogue)
    assert "Hero" in dialogue[0] or "Villain" in dialogue[0]
    print("  ✓ Basic dialogue generation")
    
    # Test with use_advanced=False (should still work)
    dialogue = gen.generate_dialogue(
        "Hero", "Villain",
        context="conflict",
        use_advanced=False,
        num_lines=4
    )
    assert len(dialogue) > 0
    print("  ✓ Advanced flag with no LLM (falls back to templates)")
    
    # Test different contexts
    contexts = ["conflict", "revelation", "emotional", "romantic", "mysterious"]
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
    
    # Test has_llm method
    assert gen.has_llm() is False
    assert gen.get_llm_info()["available"] is False
    print("  ✓ LLM status methods")
    
    print("✅ DialogueGenerator (Legacy) tests passed!\n")


def test_dialogue_generator_with_mock_llm():
    """Test DialogueGenerator with Mock LLM (advanced mode)"""
    print("\n🤖 Testing DialogueGenerator with Mock LLM...")
    
    # Create mock LLM backend
    mock_llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    gen = DialogueGenerator(llm_backend=mock_llm)
    
    # Test that LLM is detected
    assert gen.has_llm() is True
    info = gen.get_llm_info()
    assert info["available"] is True
    assert info["provider"] == "mock"
    print("  ✓ LLM detection")
    
    # Test advanced dialogue generation
    dialogue = gen.generate_dialogue(
        "Hero", "Villain",
        context="conflict",
        use_advanced=True,
        style="dramatic",
        num_lines=5
    )
    assert len(dialogue) > 0
    assert isinstance(dialogue, list)
    print("  ✓ Advanced dialogue generation")
    
    # Test template mode still works
    dialogue_template = gen.generate_dialogue(
        "Hero", "Villain",
        context="conflict",
        use_advanced=False,
        num_lines=3
    )
    assert len(dialogue_template) > 0
    print("  ✓ Template mode still works")
    
    # Test monologue with LLM
    monologue = gen.generate_monologue("Hero", "destiny", "reflective", use_advanced=True)
    assert len(monologue) > 0
    print("  ✓ Advanced monologue generation")
    
    print("✅ DialogueGenerator with Mock LLM tests passed!\n")


def test_toolkit_integration():
    """Test integration with StoryToolkit"""
    print("\n🔧 Testing StoryToolkit Integration...")
    
    from story_toolkit import StoryToolkit
    
    # Test without LLM
    toolkit = StoryToolkit()
    assert toolkit._llm_backend is None
    assert toolkit.dialogue_gen.use_llm is False
    
    # Test creating story
    story = toolkit.create_story("fantasy", "courage")
    assert story is not None
    assert story["metadata"]["genre"] == "fantasy"
    assert story["metadata"]["has_llm"] is False
    print("  ✓ Toolkit without LLM")
    
    # Test with Mock LLM
    mock_llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit_advanced = StoryToolkit(llm_backend=mock_llm)
    
    assert toolkit_advanced._llm_backend is not None
    status = toolkit_advanced.get_llm_status()
    assert status["available"] is True
    
    # Test advanced dialogue generation
    dialogue = toolkit_advanced.generate_advanced_dialogue(
        "Hero", "Villain",
        context="conflict",
        style="dramatic",
        num_lines=4
    )
    assert len(dialogue) > 0
    print("  ✓ Toolkit advanced dialogue")
    
    # Test full story generation with advanced dialogue
    story = toolkit_advanced.generate_full_story(
        genre="fantasy",
        theme="courage",
        num_characters=2,
        use_advanced_dialogue=True
    )
    assert story is not None
    assert story["metadata"]["has_llm"] is True
    print("  ✓ Full story with advanced dialogue")
    
    print("✅ Toolkit integration tests passed!\n")


def test_backward_compatibility():
    """Test that old code still works"""
    print("\n🔄 Testing Backward Compatibility...")
    
    from story_toolkit import StoryToolkit
    from story_toolkit.core.character import Character
    
    # Old way of using the library (v1.0.0 style)
    toolkit = StoryToolkit()
    
    # Create story the old way
    story = toolkit.create_story("fantasy", "courage")
    assert story is not None
    
    # Add character the old way
    hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
    hero.add_trait("brave")
    
    # Generate dialogue the old way (no use_advanced parameter)
    dialogue = toolkit.dialogue_gen.generate_dialogue("Kai", "Villain", context="conflict")
    assert len(dialogue) > 0
    
    # Check coherence the old way
    report = toolkit.check_story_coherence(story)
    assert report is not None
    
    print("  ✓ All old-style calls still work")
    print("✅ Backward compatibility tests passed!\n")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 STORY TOOLKIT v2.0.0 - GENERATOR TESTS")
    print("="*50)
    
    test_character_generator()
    test_plot_generator()
    test_dialogue_generator_without_llm()
    test_dialogue_generator_with_mock_llm()
    test_toolkit_integration()
    test_backward_compatibility()
    
    print("="*50)
    print("✅ All generator tests passed!")
    print("="*50 + "\n")