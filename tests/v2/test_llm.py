"""
Tests for v2.0.0 - LLM Layer (Mock backend)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit.llm import LLMFactory, LLMProvider
from story_toolkit import StoryToolkit


def test_llm_imports():
    print("\n🤖 Testing LLM Imports (v2)...")
    
    from story_toolkit.llm import BaseLLMBackend, LLMConfig
    assert LLMFactory is not None
    assert LLMProvider is not None
    
    print("   ✅ LLM imports passed")
    return True


def test_mock_backend():
    print("\n🔧 Testing Mock Backend (v2)...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    response = llm.generate("Hello")
    dialogue = llm.generate_dialogue("Hero", "Villain", "conflict", num_lines=3)
    
    assert response is not None
    assert len(dialogue) == 3
    
    print("   ✅ Mock backend tests passed")
    return True


def test_llm_dialogue():
    print("\n💬 Testing LLM Dialogue (v2)...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    dialogue = toolkit.dialogue_gen.generate_dialogue(
        "Hero", "Villain",
        context="conflict",
        use_advanced=True,
        style="dramatic",
        num_lines=3
    )
    
    assert len(dialogue) == 3
    assert toolkit.get_llm_status()["available"] is True
    
    print("   ✅ LLM dialogue tests passed")
    return True


def test_backward_compatibility():
    print("\n🔄 Testing Backward Compatibility (v1 -> v2)...")
    
    # Old way (no LLM)
    toolkit = StoryToolkit()
    story = toolkit.create_story("fantasy", "courage")
    hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
    
    assert story["metadata"]["genre"] == "fantasy"
    assert hero.name == "Kai"
    
    print("   ✅ v1 code still works in v2")
    return True


def run_all():
    print("\n" + "="*60)
    print("🧪 V2.0.0 - LLM LAYER TESTS")
    print("="*60)
    
    results = []
    results.append(("LLM Imports", test_llm_imports()))
    results.append(("Mock Backend", test_mock_backend()))
    results.append(("LLM Dialogue", test_llm_dialogue()))
    results.append(("Backward Compatibility", test_backward_compatibility()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2 Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    run_all()
