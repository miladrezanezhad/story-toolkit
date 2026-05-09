"""
Tests for v2.0.0 - LLM Core (Mock Backend, Basic Functionality)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit.llm import LLMFactory, LLMProvider
from story_toolkit import StoryToolkit
from story_toolkit.generators.dialogue_generator import DialogueGenerator  # <-- ADD THIS


def test_llm_imports():
    """Test LLM module imports"""
    print("\n🤖 1. Testing LLM Imports...")
    
    from story_toolkit.llm import BaseLLMBackend, LLMConfig
    assert LLMFactory is not None
    assert LLMProvider is not None
    assert LLMConfig is not None
    
    print("   ✅ LLM imports passed")
    return True


def test_mock_backend_creation():
    """Test Mock backend creation"""
    print("\n🔧 2. Testing Mock Backend Creation...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    assert llm is not None
    assert llm.config.provider == LLMProvider.MOCK
    
    print("   ✅ Mock backend created")
    return True


def test_mock_backend_generate():
    """Test Mock backend generate method"""
    print("\n📝 3. Testing Mock Backend Generate...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    response = llm.generate("Write a short story")
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    print(f"   ✅ Generate response: {response[:50]}...")
    return True


def test_mock_backend_dialogue():
    """Test Mock backend dialogue generation"""
    print("\n💬 4. Testing Mock Backend Dialogue...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    dialogue = llm.generate_dialogue("Hero", "Villain", "conflict", num_lines=3)
    
    assert len(dialogue) == 3
    assert "Hero" in dialogue[0] or "Villain" in dialogue[0]
    
    print("   ✅ Dialogue generation works")
    for line in dialogue:
        print(f"      {line}")
    return True


def test_mock_backend_different_contexts():
    """Test Mock backend with different dialogue contexts"""
    print("\n🎭 5. Testing Mock Backend - All Contexts...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    contexts = ["conflict", "friendship", "love", "betrayal"]
    
    for context in contexts:
        dialogue = llm.generate_dialogue("A", "B", context, num_lines=2)
        assert len(dialogue) == 2
        print(f"      ✓ {context} context works")
    
    print("   ✅ All dialogue contexts work")
    return True


def test_toolkit_with_mock_llm():
    """Test StoryToolkit with Mock LLM"""
    print("\n🚀 6. Testing StoryToolkit with Mock LLM...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    # Check LLM status
    status = toolkit.get_llm_status()
    assert status["available"] is True
    assert status["provider"] == "mock"
    
    print(f"   ✅ LLM Status: {status}")
    return True


def test_advanced_dialogue_method():
    """Test generate_advanced_dialogue method"""
    print("\n💬 7. Testing generate_advanced_dialogue...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    dialogue = toolkit.generate_advanced_dialogue(
        "Knight", "Dragon",
        context="final_battle",
        style="dramatic",
        num_lines=4
    )
    
    assert len(dialogue) == 4
    assert "Knight" in dialogue[0] or "Dragon" in dialogue[0]
    
    print("   ✅ Advanced dialogue generated")
    for line in dialogue:
        print(f"      {line}")
    return True


def test_dialogue_styles():
    """Test all dialogue styles"""
    print("\n🎨 8. Testing All Dialogue Styles...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    styles = ["natural", "dramatic", "poetic", "humorous"]
    
    for style in styles:
        dialogue = toolkit.dialogue_gen.generate_dialogue(
            "Hero", "Villain",
            context="conflict",
            use_advanced=True,
            style=style,
            num_lines=3
        )
        assert len(dialogue) == 3
        print(f"      ✓ {style} style works")
    
    print("   ✅ All dialogue styles work")
    return True


def test_llm_info_methods():
    """Test has_llm and get_llm_info methods"""
    print("\nℹ️ 9. Testing LLM Info Methods...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    gen = DialogueGenerator(llm_backend=llm)  # Now works after import
    
    assert gen.has_llm() is True
    info = gen.get_llm_info()
    assert info["available"] is True
    assert info["provider"] == "mock"
    
    print(f"   ✅ LLM Info: {info}")
    return True


def run_all():
    """Run all v2 core tests"""
    print("\n" + "="*60)
    print("🧪 V2.0.0 - LLM CORE TESTS")
    print("="*60)
    
    results = []
    results.append(("LLM Imports", test_llm_imports()))
    results.append(("Mock Backend Creation", test_mock_backend_creation()))
    results.append(("Mock Backend Generate", test_mock_backend_generate()))
    results.append(("Mock Backend Dialogue", test_mock_backend_dialogue()))
    results.append(("Different Contexts", test_mock_backend_different_contexts()))
    results.append(("Toolkit with Mock LLM", test_toolkit_with_mock_llm()))
    results.append(("Advanced Dialogue", test_advanced_dialogue_method()))
    results.append(("Dialogue Styles", test_dialogue_styles()))
    results.append(("LLM Info Methods", test_llm_info_methods()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2 Core Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)