"""
Tests for v2.0.0 - LLM Integration with v1 Components

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit.llm import LLMFactory, LLMProvider
from story_toolkit import StoryToolkit
from story_toolkit.core.character import Character
from story_toolkit.core.plot import Plot
from story_toolkit.core.world_builder import WorldBuilder


def test_llm_with_character():
    """Test LLM-generated dialogue using v1 Character objects"""
    print("\n🎭 1. Testing LLM with Character objects...")
    
    # Create v1 characters
    hero = Character("Kai", 25, "protagonist")
    hero.add_trait("brave")
    hero.add_goal("Save the kingdom")
    
    villain = Character("Shadow Lord", 50, "antagonist")
    villain.add_trait("cunning")
    
    # Create LLM backend
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    # Generate dialogue between v1 characters
    dialogue = toolkit.generate_advanced_dialogue(
        hero.name, villain.name,
        context="confrontation",
        style="dramatic",
        num_lines=4
    )
    
    assert len(dialogue) == 4
    assert hero.name in dialogue[0] or villain.name in dialogue[0]
    
    print(f"   ✅ Dialogue between {hero.name} and {villain.name}")
    for line in dialogue:
        print(f"      {line}")
    return True


def test_llm_with_plot():
    """Test LLM enhancing plot descriptions"""
    print("\n📚 2. Testing LLM with Plot objects...")
    
    # Create v1 plot
    plot = Plot()
    point = plot.add_plot_point("The Discovery", "Hero finds the map", 3, 8)
    
    # Create LLM backend
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    # Enhance plot description with LLM
    enhanced = llm.generate(f"Enhance this plot description: {point.description}")
    assert enhanced is not None
    
    print(f"   ✅ Original: {point.description}")
    print(f"   ✅ Enhanced: {enhanced[:100]}...")
    return True


def test_llm_with_world_builder():
    """Test LLM generating world descriptions"""
    print("\n🌍 3. Testing LLM with WorldBuilder...")
    
    # Create v1 world
    world = WorldBuilder()
    world.create_world("Eldoria", "fantasy")
    world.add_location("Crystal City", "Ancient metropolis", "city")
    
    # Create LLM backend
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    
    # Generate location description with LLM
    enhanced = llm.generate(f"Describe this fantasy location: {world.locations[0].name}")
    assert enhanced is not None
    
    print(f"   ✅ Location: {world.locations[0].name}")
    print(f"   ✅ Generated description: {enhanced[:100]}...")
    return True


def test_llm_with_story_creation():
    """Test LLM-enhanced story creation"""
    print("\n📖 4. Testing LLM with Full Story Creation...")
    
    # Create v1 story
    toolkit = StoryToolkit()
    story = toolkit.create_story("fantasy", "courage", complexity=3)
    
    # Add v1 character
    hero = toolkit.add_character_to_story(story, "Aria", "protagonist")
    hero.add_trait("brave")
    
    # Add LLM to enhance
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit_ai = StoryToolkit(llm_backend=llm)
    
    # Generate advanced dialogue using the story's character
    dialogue = toolkit_ai.generate_advanced_dialogue(
        hero.name, "Villain",
        context="final_battle",
        style="dramatic",
        num_lines=5
    )
    
    assert len(dialogue) == 5
    print(f"   ✅ Story created with v1, dialogue enhanced with v2")
    for line in dialogue[:2]:
        print(f"      {line}")
    return True


def test_backward_compatibility_with_llm():
    """Test that v1 code still works after adding LLM"""
    print("\n🔄 5. Testing Backward Compatibility...")
    
    # v1 style (no LLM)
    toolkit_v1 = StoryToolkit()
    story_v1 = toolkit_v1.create_story("fantasy", "courage")
    hero_v1 = toolkit_v1.add_character_to_story(story_v1, "Kai", "protagonist")
    hero_v1.add_trait("brave")
    
    # Same code should work with v2 (LLM available but not used)
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit_v2 = StoryToolkit(llm_backend=llm)
    story_v2 = toolkit_v2.create_story("fantasy", "courage")
    hero_v2 = toolkit_v2.add_character_to_story(story_v2, "Kai", "protagonist")
    hero_v2.add_trait("brave")
    
    # Traditional dialogue should still work
    dialogue_v1 = toolkit_v1.dialogue_gen.generate_dialogue("Kai", "Villain", "conflict")
    dialogue_v2 = toolkit_v2.dialogue_gen.generate_dialogue("Kai", "Villain", "conflict")
    
    assert len(dialogue_v1) == len(dialogue_v2)
    
    print("   ✅ v1 code works unchanged in v2")
    return True


def test_mixed_dialogue_modes():
    """Test mixing v1 template and v2 LLM dialogue in same story"""
    print("\n🔀 6. Testing Mixed Dialogue Modes...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    # Create story with v1 components
    story = toolkit.create_story("fantasy", "courage")
    hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
    
    # Template-based dialogue (v1 style)
    template_dialogue = toolkit.dialogue_gen.generate_dialogue(
        hero.name, "Guard",
        context="conflict",
        use_advanced=False
    )
    
    # Advanced dialogue (v2 style)
    advanced_dialogue = toolkit.dialogue_gen.generate_dialogue(
        hero.name, "Villain",
        context="final_battle",
        use_advanced=True,
        style="dramatic"
    )
    
    assert len(template_dialogue) > 0
    assert len(advanced_dialogue) > 0
    
    print("   ✅ Template dialogue (v1) works alongside advanced dialogue (v2)")
    print(f"      Template: {template_dialogue[0][:50]}...")
    print(f"      Advanced: {advanced_dialogue[0][:50]}...")
    return True


def test_llm_status_with_v1_components():
    """Test LLM status when using v1 components"""
    print("\n📊 7. Testing LLM Status with v1 Components...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    status = toolkit.get_llm_status()
    assert status["available"] is True
    
    # v1 component should not affect LLM status
    story = toolkit.create_story("fantasy", "courage")
    hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
    
    status_after = toolkit.get_llm_status()
    assert status_after["available"] is True
    
    print(f"   ✅ LLM Status maintained: {status}")
    return True


def run_all():
    """Run all v2 integration tests"""
    print("\n" + "="*60)
    print("🧪 V2.0.0 - LLM INTEGRATION TESTS (v1 + v2)")
    print("="*60)
    
    results = []
    results.append(("LLM with Character", test_llm_with_character()))
    results.append(("LLM with Plot", test_llm_with_plot()))
    results.append(("LLM with WorldBuilder", test_llm_with_world_builder()))
    results.append(("LLM with Story Creation", test_llm_with_story_creation()))
    results.append(("Backward Compatibility", test_backward_compatibility_with_llm()))
    results.append(("Mixed Dialogue Modes", test_mixed_dialogue_modes()))
    results.append(("LLM Status with v1", test_llm_status_with_v1_components()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2 Integration Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)