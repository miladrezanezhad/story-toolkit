# test_llm_quick.py
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

print("="*50)
print("TESTING LLM LAYER - MOCK MODE")
print("="*50)

# 1. Create mock backend
print("\n1️⃣ Creating Mock LLM Backend...")
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
print("   ✅ Mock backend created")

# 2. Test simple generation
print("\n2️⃣ Testing simple text generation...")
response = llm.generate("Write a short story")
print(f"   📝 Output: {response[:100]}...")
print("   ✅ Text generation works")

# 3. Test dialogue generation
print("\n3️⃣ Testing dialogue generation...")
dialogue = llm.generate_dialogue("Hero", "Villain", "conflict", num_lines=3)
print("   💬 Generated dialogue:")
for line in dialogue:
    print(f"      {line}")
print("   ✅ Dialogue generation works")

# 4. Test Toolkit integration
print("\n4️⃣ Testing integration with StoryToolkit...")
toolkit = StoryToolkit(llm_backend=llm)
status = toolkit.get_llm_status()
print(f"   📊 LLM Status: {status}")
assert status["available"] is True
print("   ✅ Toolkit integration successful")

print("\n" + "="*50)
print("✅ All LLM layer tests passed!")
print("="*50)
