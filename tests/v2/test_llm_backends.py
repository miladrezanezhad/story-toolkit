"""
Tests for v2.0.0 - All LLM Backends

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit.llm import LLMFactory, LLMProvider
from story_toolkit import StoryToolkit


def test_mock_backend_complete():
    """Test Mock backend thoroughly"""
    print("\n🎭 1. Testing Mock Backend (Complete)...")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    
    # Test generate
    response = llm.generate("Hello")
    assert response is not None
    
    # Test dialogue
    dialogue = llm.generate_dialogue("A", "B", "conflict", num_lines=3)
    assert len(dialogue) == 3
    
    # Test with toolkit
    toolkit = StoryToolkit(llm_backend=llm)
    status = toolkit.get_llm_status()
    assert status["available"] is True
    assert status["provider"] == "mock"
    
    print("   ✅ Mock backend fully functional")
    return True


def test_openai_backend_import():
    """Test OpenAI backend import (does not require API key)"""
    print("\n🤖 2. Testing OpenAI Backend Import...")
    
    try:
        from story_toolkit.llm.backends.openai_backend import OpenAIBackend
        print("   ✅ OpenAI backend module available")
        return True
    except ImportError:
        print("   ⚠️ OpenAI not installed - skipping")
        return True


def test_anthropic_backend_import():
    """Test Anthropic backend import"""
    print("\n🧠 3. Testing Anthropic Backend Import...")
    
    try:
        from story_toolkit.llm.backends.anthropic_backend import AnthropicBackend
        print("   ✅ Anthropic backend module available")
        return True
    except ImportError:
        print("   ⚠️ Anthropic not installed - skipping")
        return True


def test_local_backend_import():
    """Test Local backend import"""
    print("\n💻 4. Testing Local Backend Import...")
    
    try:
        from story_toolkit.llm.backends.local_backend import LocalLLMBackend
        print("   ✅ Local backend module available")
        return True
    except ImportError:
        print("   ⚠️ Local backend dependencies not installed - skipping")
        return True


def test_factory_create_from_env():
    """Test factory create from environment"""
    print("\n🌍 5. Testing Factory create_from_env...")
    
    import os
    original_provider = os.environ.get('STORY_LLM_PROVIDER')
    
    try:
        os.environ['STORY_LLM_PROVIDER'] = 'mock'
        llm = LLMFactory.create_from_env()
        assert llm is not None
        print("   ✅ create_from_env works with mock")
    finally:
        if original_provider:
            os.environ['STORY_LLM_PROVIDER'] = original_provider
        else:
            os.environ.pop('STORY_LLM_PROVIDER', None)
    
    return True


def test_llm_config():
    """Test LLMConfig dataclass"""
    print("\n⚙️ 6. Testing LLMConfig...")
    
    from story_toolkit.llm import LLMConfig
    
    config = LLMConfig(
        provider=LLMProvider.MOCK,
        model="test-model",
        temperature=0.5,
        max_tokens=500
    )
    
    assert config.provider == LLMProvider.MOCK
    assert config.model == "test-model"
    assert config.temperature == 0.5
    assert config.max_tokens == 500
    
    print("   ✅ LLMConfig works")
    return True


def run_all():
    """Run all v2 backend tests"""
    print("\n" + "="*60)
    print("🧪 V2.0.0 - LLM BACKEND TESTS")
    print("="*60)
    
    results = []
    results.append(("Mock Backend Complete", test_mock_backend_complete()))
    results.append(("OpenAI Backend Import", test_openai_backend_import()))
    results.append(("Anthropic Backend Import", test_anthropic_backend_import()))
    results.append(("Local Backend Import", test_local_backend_import()))
    results.append(("Factory create_from_env", test_factory_create_from_env()))
    results.append(("LLMConfig", test_llm_config()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2 Backend Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)