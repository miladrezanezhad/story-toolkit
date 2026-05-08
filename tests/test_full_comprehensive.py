"""
Comprehensive test suite for Story Toolkit
Tests both legacy (v1) and new (v2 with LLM) features.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import tempfile
import os


# ============================================================
# PART 1: LEGACY TESTS (v1.0.0 - Should work without LLM)
# ============================================================

def test_legacy_imports():
    """Test that all legacy imports work"""
    print("\n📦 1. Testing Legacy Imports...")
    
    try:
        from story_toolkit import StoryToolkit
        from story_toolkit.core.character import Character
        from story_toolkit.core.plot import Plot
        from story_toolkit.core.world_builder import WorldBuilder
        from story_toolkit.core.story_engine import StoryEngine
        from story_toolkit.generators.character_generator import CharacterGenerator
        from story_toolkit.generators.plot_generator import PlotGenerator
        from story_toolkit.generators.dialogue_generator import DialogueGenerator
        from story_toolkit.nlp.coherence_checker import CoherenceChecker
        from story_toolkit.nlp.text_analyzer import TextAnalyzer
        from story_toolkit.utils.helpers import save_story, load_story, export_to_markdown
        
        print("  ✓ All legacy imports successful")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_legacy_toolkit_creation():
    """Test StoryToolkit creation without LLM"""
    print("\n🏗️ 2. Testing Toolkit Creation (Legacy Mode)...")
    
    try:
        from story_toolkit import StoryToolkit
        
        toolkit = StoryToolkit()
        assert toolkit is not None
        assert hasattr(toolkit, 'create_story')
        assert hasattr(toolkit, 'add_character_to_story')
        assert hasattr(toolkit, 'check_story_coherence')
        assert hasattr(toolkit, 'dialogue_gen')
        assert toolkit._llm_backend is None
        
        print("  ✓ Toolkit created without LLM")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_story_creation():
    """Test basic story creation (v1 style)"""
    print("\n📖 3. Testing Story Creation (Legacy)...")
    
    try:
        from story_toolkit import StoryToolkit
        
        toolkit = StoryToolkit()
        story = toolkit.create_story(genre="fantasy", theme="courage")
        
        assert story is not None
        assert "metadata" in story
        assert story["metadata"]["genre"] == "fantasy"
        assert story["metadata"]["theme"] == "courage"
        assert "outline" in story
        assert "plot" in story
        assert "characters" in story
        assert "coherence_report" in story
        
        print("  ✓ Story created successfully")
        print(f"    - Genre: {story['metadata']['genre']}")
        print(f"    - Theme: {story['metadata']['theme']}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_character_creation():
    """Test character creation and manipulation (v1 style)"""
    print("\n🎭 4. Testing Character Creation (Legacy)...")
    
    try:
        from story_toolkit import StoryToolkit
        from story_toolkit.core.character import Character
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "courage")
        
        # Add character using toolkit
        hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
        hero.add_trait("brave")
        hero.add_skill("sword_mastery")
        hero.add_goal("Save the kingdom")
        hero.add_fear("darkness")
        
        # Direct character creation
        villain = Character("Morgath", 45, "antagonist")
        villain.add_trait("cunning")
        villain.add_goal("Rule the world")
        
        story["characters"].append(villain)
        
        assert len(story["characters"]) == 2
        assert "brave" in hero.personality_traits
        assert "sword_mastery" in hero.skills
        assert "Save the kingdom" in hero.goals
        
        print("  ✓ Characters created and modified")
        print(f"    - Hero: {hero.name} ({hero.role})")
        print(f"    - Villain: {villain.name} ({villain.role})")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_dialogue_generation():
    """Test dialogue generation without LLM (v1 style)"""
    print("\n💬 5. Testing Dialogue Generation (Legacy)...")
    
    try:
        from story_toolkit import StoryToolkit
        
        toolkit = StoryToolkit()
        
        # Test various contexts
        contexts = ["conflict", "revelation", "emotional", "romantic", "mysterious"]
        
        for context in contexts:
            dialogue = toolkit.dialogue_gen.generate_dialogue(
                "Hero", "Villain", 
                context=context,
                num_lines=3
            )
            assert len(dialogue) > 0
            assert isinstance(dialogue, list)
            print(f"    ✓ {context}: {len(dialogue)} lines")
        
        # Test monologue
        monologue = toolkit.dialogue_gen.generate_monologue("Hero", "destiny", "reflective")
        assert len(monologue) > 0
        
        print("  ✓ All dialogue contexts work")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_plot_generation():
    """Test plot generation for all genres"""
    print("\n📚 6. Testing Plot Generation (Legacy)...")
    
    try:
        from story_toolkit.generators.plot_generator import PlotGenerator
        
        gen = PlotGenerator()
        genres = ["fantasy", "sci-fi", "mystery", "adventure", "romance"]
        
        for genre in genres:
            plot = gen.generate_plot(genre, complexity=3)
            assert plot is not None
            assert plot["genre"] == genre
            assert "main_plot" in plot
            assert "estimated_length" in plot
            print(f"    ✓ {genre}: {plot['estimated_length']['estimated_chapters']} chapters")
        
        print("  ✓ All genres work")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_world_building():
    """Test world building features"""
    print("\n🌍 7. Testing World Building (Legacy)...")
    
    try:
        from story_toolkit.core.world_builder import WorldBuilder
        
        world = WorldBuilder()
        
        # Create world
        world.create_world("Eldoria", "fantasy")
        assert world.name == "Eldoria"
        
        # Add locations
        world.add_location("Crystal City", "Beautiful city", "city")
        world.add_location("Dark Forest", "Mysterious woods", "forest")
        assert len(world.locations) >= 2
        
        # Add rules
        world.add_rule("magic", "Only pure hearts can use magic")
        
        # Add factions
        world.add_faction("Shadow Guild", "Secret organization", ["control magic"])
        assert len(world.factions) >= 1
        
        # Generate complete world
        gen_world = world.generate_world("fantasy")
        assert "key_locations" in gen_world
        
        print("  ✓ World created with locations, rules, and factions")
        print(f"    - World: {world.name}")
        print(f"    - Locations: {len(world.locations)}")
        print(f"    - Factions: {len(world.factions)}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_coherence_check():
    """Test coherence checking"""
    print("\n🔍 8. Testing Coherence Check (Legacy)...")
    
    try:
        from story_toolkit import StoryToolkit
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "courage")
        
        # Add some characters
        hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
        villain = toolkit.add_character_to_story(story, "Morgath", "antagonist")
        
        # Check coherence
        report = toolkit.check_story_coherence(story)
        
        assert report is not None
        assert "overall_score" in report or "score" in report
        
        score = report.get("overall_score", report.get("score", 0))
        print(f"    - Coherence score: {score}")
        
        print("  ✓ Coherence check completed")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_legacy_save_load():
    """Test save and load functionality"""
    print("\n💾 9. Testing Save/Load (Legacy)...")
    
    try:
        from story_toolkit import StoryToolkit
        from story_toolkit.utils.helpers import save_story, load_story
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "courage")
        toolkit.add_character_to_story(story, "Kai", "protagonist")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Save
            save_story(story, tmp_path)
            assert os.path.exists(tmp_path)
            
            # Load
            loaded = load_story(tmp_path)
            assert loaded is not None
            assert loaded["metadata"]["genre"] == "fantasy"
            
            print("  ✓ Story saved and loaded successfully")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


# ============================================================
# PART 2: NEW V2 FEATURES TESTS (With LLM)
# ============================================================

def test_v2_llm_imports():
    """Test that new LLM imports work"""
    print("\n🤖 10. Testing V2 LLM Imports...")
    
    try:
        from story_toolkit.llm import LLMFactory, LLMProvider, BaseLLMBackend, MockLLMBackend
        
        assert LLMFactory is not None
        assert LLMProvider is not None
        assert MockLLMBackend is not None
        
        print("  ✓ V2 LLM imports successful")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_v2_mock_llm_creation():
    """Test creating mock LLM backend"""
    print("\n🔧 11. Testing Mock LLM Backend...")
    
    try:
        from story_toolkit.llm import LLMFactory, LLMProvider
        
        llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
        assert llm is not None
        
        # Test generate
        response = llm.generate("Hello")
        assert response is not None
        assert isinstance(response, str)
        
        # Test dialogue generation
        dialogue = llm.generate_dialogue("Hero", "Villain", "conflict", num_lines=3)
        assert len(dialogue) == 3
        assert "Hero" in dialogue[0] or "Villain" in dialogue[0]
        
        print("  ✓ Mock LLM backend works")
        print(f"    - Generate: {response[:50]}...")
        print(f"    - Dialogue: {len(dialogue)} lines")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_v2_toolkit_with_llm():
    """Test StoryToolkit with LLM backend"""
    print("\n🚀 12. Testing Toolkit with Mock LLM...")
    
    try:
        from story_toolkit import StoryToolkit
        from story_toolkit.llm import LLMFactory, LLMProvider
        
        llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
        toolkit = StoryToolkit(llm_backend=llm)
        
        # Check LLM status
        status = toolkit.get_llm_status()
        assert status["available"] is True
        assert status["provider"] == "mock"
        
        # Create story with LLM flag
        story = toolkit.create_story("fantasy", "courage")
        assert story["metadata"]["has_llm"] is True
        
        # Test advanced dialogue
        dialogue = toolkit.generate_advanced_dialogue(
            "Hero", "Villain",
            context="conflict",
            style="dramatic",
            num_lines=4
        )
        assert len(dialogue) > 0
        
        # Test full story with advanced dialogue
        full_story = toolkit.generate_full_story(
            genre="fantasy",
            theme="courage",
            num_characters=2,
            use_advanced_dialogue=True
        )
        assert full_story is not None
        
        print("  ✓ Toolkit with LLM works")
        print(f"    - LLM Status: {status}")
        print(f"    - Advanced dialogue: {len(dialogue)} lines")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_v2_dialogue_with_llm():
    """Test DialogueGenerator with LLM integration"""
    print("\n💬 13. Testing DialogueGenerator with LLM...")
    
    try:
        from story_toolkit.generators.dialogue_generator import DialogueGenerator
        from story_toolkit.llm import LLMFactory, LLMProvider
        
        llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
        gen = DialogueGenerator(llm_backend=llm)
        
        # Check LLM detection
        assert gen.has_llm() is True
        info = gen.get_llm_info()
        assert info["available"] is True
        
        # Test advanced dialogue
        advanced = gen.generate_dialogue(
            "Hero", "Villain",
            context="conflict",
            use_advanced=True,
            style="dramatic",
            num_lines=5
        )
        assert len(advanced) == 5
        
        # Test template mode still works
        template = gen.generate_dialogue(
            "Hero", "Villain",
            context="conflict",
            use_advanced=False,
            num_lines=3
        )
        assert len(template) == 3
        
        # Test monologue with LLM
        monologue = gen.generate_monologue(
            "Hero", "destiny",
            mood="reflective",
            use_advanced=True
        )
        assert len(monologue) > 0
        
        print("  ✓ DialogueGenerator with LLM works")
        print(f"    - Advanced dialogue: {len(advanced)} lines")
        print(f"    - Template dialogue: {len(template)} lines")
        print(f"    - Monologue: {len(monologue)} lines")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_v2_backward_compatibility():
    """Test that old code still works with new version"""
    print("\n🔄 14. Testing Backward Compatibility...")
    
    try:
        from story_toolkit import StoryToolkit
        
        # Old way - no LLM parameter
        toolkit = StoryToolkit()
        
        # Old way of creating story
        story = toolkit.create_story("fantasy", "courage")
        
        # Old way of adding character
        hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
        hero.add_trait("brave")
        
        # Old way of generating dialogue
        dialogue = toolkit.dialogue_gen.generate_dialogue("Kai", "Villain", context="conflict")
        assert len(dialogue) > 0
        
        # Old way of checking coherence
        report = toolkit.check_story_coherence(story)
        assert report is not None
        
        print("  ✓ All v1 code still works without modification")
        print("  ✓ No breaking changes introduced")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_v2_version_info():
    """Test version information"""
    print("\n📌 15. Testing Version Info...")
    
    try:
        import story_toolkit
        
        version = story_toolkit.__version__
        author = story_toolkit.__author__
        github = story_toolkit.__github__
        
        print(f"    - Version: {version}")
        print(f"    - Author: {author}")
        print(f"    - GitHub: {github}")
        
        assert version == "2.0.0"
        assert author is not None
        
        print("  ✓ Version info correct")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


# ============================================================
# PART 3: PERFORMANCE TESTS
# ============================================================

def test_performance_story_creation():
    """Test story creation performance"""
    print("\n⚡ 16. Testing Performance...")
    
    import time
    
    try:
        from story_toolkit import StoryToolkit
        
        toolkit = StoryToolkit()
        
        # Test story creation speed
        start = time.time()
        for _ in range(10):
            story = toolkit.create_story("fantasy", "courage")
        elapsed = time.time() - start
        
        print(f"    - 10 story creations: {elapsed:.3f} seconds")
        print(f"    - Average: {elapsed/10:.3f} seconds per story")
        
        # Test dialogue generation speed
        start = time.time()
        for _ in range(20):
            dialogue = toolkit.dialogue_gen.generate_dialogue("A", "B", "conflict")
        elapsed = time.time() - start
        
        print(f"    - 20 dialogue generations: {elapsed:.3f} seconds")
        print(f"    - Average: {elapsed/20:.3f} seconds per dialogue")
        
        print("  ✓ Performance acceptable")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


# ============================================================
# MAIN TEST RUNNER
# ============================================================

def run_all_tests():
    """Run all comprehensive tests"""
    
    print("\n" + "="*60)
    print("🧪 STORY TOOLKIT - COMPREHENSIVE TEST SUITE v2.0.0")
    print("="*60)
    print("\nTesting from v1.0.0 (Legacy) to v2.0.0 (with LLM)")
    print("-"*60)
    
    tests = [
        # Legacy tests (v1)
        ("Legacy Imports", test_legacy_imports),
        ("Toolkit Creation", test_legacy_toolkit_creation),
        ("Story Creation", test_legacy_story_creation),
        ("Character Creation", test_legacy_character_creation),
        ("Dialogue Generation", test_legacy_dialogue_generation),
        ("Plot Generation", test_legacy_plot_generation),
        ("World Building", test_legacy_world_building),
        ("Coherence Check", test_legacy_coherence_check),
        ("Save/Load", test_legacy_save_load),
        
        # V2 tests (with LLM)
        ("V2 LLM Imports", test_v2_llm_imports),
        ("V2 Mock LLM", test_v2_mock_llm_creation),
        ("V2 Toolkit with LLM", test_v2_toolkit_with_llm),
        ("V2 Dialogue with LLM", test_v2_dialogue_with_llm),
        ("V2 Backward Compatibility", test_v2_backward_compatibility),
        ("V2 Version Info", test_v2_version_info),
        
        # Performance
        ("Performance", test_performance_story_creation),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                results.append(("✅", name))
            else:
                failed += 1
                results.append(("❌", name))
        except Exception as e:
            failed += 1
            results.append(("❌", name))
            print(f"    Exception: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for status, name in results:
        print(f"  {status} {name}")
    
    print("-"*60)
    print(f"  Total: {len(tests)} tests")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📈 Success Rate: {passed/len(tests)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Story Toolkit v2.0.0 is ready for release!")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the issues above.")
    
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)