# test_openai_real.py
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# Note: This test requires an OpenAI API key
# export OPENAI_API_KEY="sk-..."

def test_real_openai():
    print("="*60)
    print("TESTING REAL OPENAI BACKEND (Requires API Key)")
    print("="*60)
    
    try:
        # Create OpenAI backend
        llm = LLMFactory.create_backend(
            provider=LLMProvider.OPENAI,
            api_key="your-openai-api-key",  # Or read from environment
            model="gpt-3.5-turbo",
            temperature=0.8
        )
        
        toolkit = StoryToolkit(llm_backend=llm)
        
        # Test real dialogue generation
        print("\n📝 Generating dialogue with ChatGPT...")
        dialogue = toolkit.generate_advanced_dialogue(
            "Brave Knight", 
            "Ancient Dragon",
            context="final_battle",
            style="epic",
            num_lines=6
        )
        
        print("\n💬 Generated dialogue:")
        for line in dialogue:
            print(f"   {line}")
        
        print("\n✅ Real OpenAI backend is working correctly!")
        
    except Exception as e:
        print(f"\n⚠️ Error connecting to OpenAI: {e}")
        print("   API key may be invalid or missing")

if __name__ == "__main__":
    test_real_openai()
