# test_llm_assertions.py
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

def run_llm_validation():
    """Automated LLM layer validation tests"""
    
    errors = []
    successes = []
    
    print("="*60)
    print("RUNNING AUTOMATED LLM LAYER TESTS")
    print("="*60)
    
    # Test 1: Create backend
    try:
        llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
        successes.append("✅ Mock Backend creation")
    except Exception as e:
        errors.append(f"❌ Mock Backend creation: {e}")
    
    # Test 2: Check backend type
    try:
        from story_toolkit.llm.base import BaseLLMBackend
        assert isinstance(llm, BaseLLMBackend)
        successes.append("✅ Backend type is correct")
    except Exception as e:
        errors.append(f"❌ Backend type: {e}")
    
    # Test 3: Text generation
    try:
        response = llm.generate("Hello")
        assert len(response) > 0
        successes.append("✅ Text generation")
    except Exception as e:
        errors.append(f"❌ Text generation: {e}")
    
    # Test 4: Dialogue generation
    try:
        dialogue = llm.generate_dialogue("A", "B", "conflict", num_lines=3)
        assert len(dialogue) == 3
        assert all(":" in line for line in dialogue)
        successes.append("✅ Dialogue generation")
    except Exception as e:
        errors.append(f"❌ Dialogue generation: {e}")
    
    # Test 5: Toolkit integration
    try:
        toolkit = StoryToolkit(llm_backend=llm)
        status = toolkit.get_llm_status()
        assert status["available"] is True
        successes.append("✅ Toolkit integration")
    except Exception as e:
        errors.append(f"❌ Toolkit integration: {e}")
    
    # Test 6: Advanced dialogue
    try:
        advanced = toolkit.dialogue_gen.generate_dialogue(
            "Hero", "Villain",
            context="conflict",
            use_advanced=True,
            num_lines=4
        )
        assert len(advanced) == 4
        successes.append("✅ Advanced dialogue")
    except Exception as e:
        errors.append(f"❌ Advanced dialogue: {e}")
    
    # Final report
    print("\n" + "-"*40)
    for s in successes:
        print(f"   {s}")
    
    if errors:
        print("\n⚠️ Errors:")
        for e in errors:
            print(f"   {e}")
    else:
        print("\n🎉 All tests passed successfully!")
    
    print("-"*40)
    print(f"📊 Summary: {len(successes)} passed, {len(errors)} failed")
    print("="*60)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = run_llm_validation()
    exit(0 if success else 1)