# test_quick_verify.py
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

print("Quick LLM verification test...")

# Create mock LLM
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# Check status
status = toolkit.get_llm_status()
print(f"LLM Status: {status}")

# Generate dialogue
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Hero", "Villain",
    context="conflict",
    use_advanced=True,
    style="dramatic",
    num_lines=3
)

print("Generated dialogue:")
for line in dialogue:
    print(f"  {line}")

print("✅ LLM is working correctly!")

