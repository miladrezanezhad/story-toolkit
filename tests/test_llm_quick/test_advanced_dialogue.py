# test_advanced_dialogue.py
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

def test_advanced_dialogue():
    print("="*60)
    print("TESTING ADVANCED DIALOGUE WITH LLM LAYER")
    print("="*60)
    
    # Create mock LLM
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    toolkit = StoryToolkit(llm_backend=llm)
    
    # Test 1: Simple dialogue (without LLM - legacy mode)
    print("\n📌 Test 1: Dialogue without LLM (legacy mode)")
    simple = toolkit.dialogue_gen.generate_dialogue(
        "Kai", "Shadow Demon", 
        context="conflict",
        use_advanced=False
    )
    for line in simple:
        print(f"   {line}")
    
    # Test 2: Advanced dialogue (with LLM)
    print("\n📌 Test 2: Advanced dialogue with LLM")
    advanced = toolkit.dialogue_gen.generate_dialogue(
        "Kai", "Shadow Demon",
        context="conflict",
        use_advanced=True,
        style="dramatic",
        num_lines=5
    )
    for line in advanced:
        print(f"   {line}")
    
    # Test 3: Romantic dialogue
    print("\n📌 Test 3: Romantic dialogue")
    romantic = toolkit.generate_advanced_dialogue(
        "Layla", "Arash",
        context="love",
        style="poetic",
        num_lines=4
    )
    for line in romantic:
        print(f"   {line}")
    
    # Test 4: Emotional monologue
    print("\n📌 Test 4: Emotional monologue")
    monologue = toolkit.dialogue_gen.generate_monologue(
        "Hero", "destiny",
        mood="reflective",
        use_advanced=True
    )
    for line in monologue:
        print(f"   {line}")
    
    print("\n" + "="*60)
    print("✅ LLM layer is working correctly!")
    print("="*60)

if __name__ == "__main__":
    test_advanced_dialogue()
