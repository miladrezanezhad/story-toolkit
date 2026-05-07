# 📚 Story Development Toolkit

[![Tests](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](https://github.com/miladrezanezhad/story-toolkit/releases)
[![Author](https://img.shields.io/badge/Author-Milad%20Rezanezhad-purple.svg)](https://github.com/miladrezanezhad)

**A comprehensive Python toolkit for generating engaging and coherent stories with optional LLM support.**

Story Development Toolkit provides tools for character creation, plot generation, dialogue writing, world building, and story coherence analysis — all in one package. **NEW in v2.0.0:** Optional integration with OpenAI, Anthropic, and local LLMs!

---

## 🌐 Language

This README is also available in:

| Language | File |
|----------|------|
| 🇮🇷 **Persian (فارسی)** | [README_FA.md](README_FA.md) |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎭 **Character Creation** | Build complex characters with traits, goals, skills, fears, relationships |
| 📚 **Plot Generation** | Generate story structures for fantasy, mystery, romance, adventure, sci-fi |
| 💬 **Dialogue Writing** | Create natural dialogues with context-aware templates |
| 🌍 **World Building** | Design detailed fictional worlds with locations, cultures, rules, factions |
| 🔍 **Coherence Checking** | Identify plot holes, character inconsistencies, timeline issues |
| 📊 **Text Analysis** | Analyze readability, pacing, dialogue balance, vocabulary richness |
| 🤖 **LLM Support** | Optional integration with OpenAI, Anthropic, and local models (NEW in v2.0.0) |

---

## 📦 Installation

```bash
# Basic installation (no LLM)
pip install story-toolkit

# With OpenAI support (GPT-4, GPT-3.5)
pip install story-toolkit[openai]

# With Anthropic support (Claude)
pip install story-toolkit[anthropic]

# With local LLM support (Ollama, llama.cpp)
pip install story-toolkit[local]

# Full installation (all LLM backends)
pip install story-toolkit[all]

# Or install from source
git clone https://github.com/miladrezanezhad/story-toolkit.git
cd story-toolkit
pip install -e .
```

---

## 🚀 Quick Start

### Basic Usage (No LLM - v1 compatible)

```python
from story_toolkit import StoryToolkit

# Create toolkit instance
toolkit = StoryToolkit()

# Create a story
story = toolkit.create_story(genre="fantasy", theme="courage")

# Add a hero
hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
hero.add_trait("brave")
hero.add_goal("Save the kingdom")

# Generate dialogue (template-based)
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Kai", "Villain", context="conflict"
)
for line in dialogue:
    print(line)

# Check coherence
report = toolkit.check_story_coherence(story)
print(f"Coherence Score: {report['overall_score']:.0%}")
```

**Output:**
```
Kai: I can't believe you would do this!
Villain: You left me no choice.
Kai: There's always a choice. You just chose wrong.
Coherence Score: 100%
```

### Advanced Usage (With LLM - NEW in v2.0.0)

```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# Create LLM backend (Mock for testing, no API key needed)
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# Generate advanced dialogue with LLM
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Kai", "Villain",
    context="final_battle",
    use_advanced=True,  # Enable LLM
    style="dramatic",
    num_lines=8
)

for line in dialogue:
    print(line)

# Check LLM status
print(f"LLM Status: {toolkit.get_llm_status()}")
```

**Output:**
```
Kai: I can't believe what you've done!
Villain: You left me no choice, Kai.
Kai: There's always a choice. You chose wrong.
Villain: We'll see who was wrong in the end.
Kai: This isn't over.
LLM Status: {'available': True, 'provider': 'mock', 'model': 'mock'}
```

---

## 🤖 LLM Backends

v2.0.0 supports multiple LLM providers:

| Provider | Installation | API Key Required |
|----------|--------------|------------------|
| **Mock** | Included | ❌ No (for testing) |
| **OpenAI** | `pip install story-toolkit[openai]` | ✅ Yes |
| **Anthropic** | `pip install story-toolkit[anthropic]` | ✅ Yes |
| **Local (Ollama)** | `pip install story-toolkit[local]` | ❌ No (free) |

### Example with OpenAI

```python
import os
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# Set your API key
os.environ["OPENAI_API_KEY"] = "sk-..."

# Create OpenAI backend
llm = LLMFactory.create_backend(
    provider=LLMProvider.OPENAI,
    model="gpt-3.5-turbo",
    temperature=0.8
)

toolkit = StoryToolkit(llm_backend=llm)

# Generate advanced dialogue
dialogue = toolkit.generate_advanced_dialogue(
    "Knight", "Dragon",
    context="final_battle",
    style="epic",
    num_lines=6
)
```

### Example with Local LLM (Ollama)

```bash
# First, install and run Ollama
ollama pull llama2
```

```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# Create local backend (free, no API key)
llm = LLMFactory.create_backend(
    provider=LLMProvider.LOCAL,
    model="llama2",
    temperature=0.7
)

toolkit = StoryToolkit(llm_backend=llm)
```

---

## 📁 Project Structure

```
story_toolkit/
├── story_toolkit/          # Main Python package
│   ├── core/               # Story engine, Character, Plot, WorldBuilder
│   ├── generators/         # Character, Plot, and Dialogue generators
│   ├── nlp/                # Coherence checker and Text analyzer
│   ├── llm/                # LLM layer (NEW in v2.0.0)
│   │   ├── base.py        # Base classes
│   │   ├── factory.py     # Backend factory
│   │   └── backends/      # Mock, OpenAI, Anthropic, Local
│   └── utils/              # Helper functions
├── docs/                   # Documentation (English & Persian)
│   ├── eng/                # English documentation
│   └── fa-ir/              # Persian documentation (مستندات فارسی)
├── examples/               # Usage examples
├── tests/                  # Unit tests
├── requirements.txt        # Dependencies
└── setup.py                # Package setup
```

---

## 📖 Documentation

Full documentation is available in two languages:

| Language | Link |
|----------|------|
| 🇬🇧 English | [docs/eng/index.html](docs/eng/index.html) |
| 🇮🇷 فارسی | [docs/fa-ir/index.html](docs/fa-ir/index.html) |

### Documentation Pages

- **Quick Start Guide** — Build your first story in 5 minutes
- **API Reference** — Complete documentation for all classes and methods
- **LLM Integration Guide** — How to use OpenAI, Anthropic, and local models
- **Examples** — Simple, complete, and advanced usage examples

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Core module tests
python -m tests.test_core

# Generator tests
python -m tests.test_generators

# NLP tool tests
python -m tests.test_nlp

# LLM layer tests
python -m tests.test_llm_quick.test_quick_verify
```

All tests should pass:
```
✅ StoryEngine tests passed!
✅ Character tests passed!
✅ Plot tests passed!
✅ WorldBuilder tests passed!
✅ LLM layer tests passed!
```

---

## 🎮 Usage Examples

### Simple Example
```bash
python -m examples.simple_example
```

### Complete Demo
```bash
python -m examples.example
```

### Advanced Features (with LLM)
```bash
python -m examples.advanced_example
```

---

## 🛠️ Core Components

### Character Development
```python
from story_toolkit.core.character import Character

hero = Character(name="Elena", age=32, role="protagonist")
hero.add_trait("brave")
hero.add_skill("sword_mastery")
hero.add_relationship("Villain", "enemy", strength=9)
hero.advance_arc()  # initial → challenged → transformation → new_equilibrium
```

### World Building
```python
from story_toolkit.core.world_builder import WorldBuilder

world = WorldBuilder()
world.create_world("Eldoria", "fantasy")
world.add_location("Crystal City", "Ancient metropolis", "city")
world.add_rule("magical", "Only eclipse-born can wield magic")
world.add_faction("Shadow Guild", "Secret organization", goals=["control_magic"])
```

### Plot Generation
```python
from story_toolkit.generators.plot_generator import PlotGenerator

gen = PlotGenerator()
plot = gen.generate_plot("mystery", complexity=4)
print(f"Estimated chapters: {plot['estimated_length']['estimated_chapters']}")
print(f"Estimated words: {plot['estimated_length']['estimated_words']:,}")
```

### Coherence Checking
```python
from story_toolkit.nlp.coherence_checker import CoherenceChecker

checker = CoherenceChecker()
report = checker.generate_coherence_report(story_data)

if report['plot_holes']:
    print("Plot holes found:")
    for hole in report['plot_holes']:
        print(f"  - {hole}")

for rec in report['recommendations']:
    print(f"💡 {rec}")
```

### LLM-Powered Dialogue (NEW)
```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# Setup LLM
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# Generate advanced dialogue
dialogue = toolkit.generate_advanced_dialogue(
    "Hero", "Villain",
    context="conflict",
    style="dramatic",
    num_lines=10
)
```

---

## 🔧 Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`:
  - `nltk>=3.8.1`
  - `spacy>=3.7.0`
  - `textblob>=0.17.1`
  - `pydantic>=2.5.0`
  - `pyyaml>=6.0`

### Optional LLM Dependencies

| Backend | Package |
|---------|---------|
| OpenAI | `openai>=1.0.0` |
| Anthropic | `anthropic>=0.18.0` |
| Local (Ollama) | `ollama>=0.1.0` |
| Local (llama.cpp) | `llama-cpp-python>=0.2.0` |

---

## 🔄 Upgrading from v1.0.0 to v2.0.0

**No breaking changes!** All v1.0.0 code continues to work unchanged.

```python
# This v1.0.0 code still works perfectly in v2.0.0
from story_toolkit import StoryToolkit

toolkit = StoryToolkit()  # No LLM by default
story = toolkit.create_story("fantasy", "courage")
# ... everything works as before
```

To use new LLM features:
```python
# Optional: Add LLM for enhanced capabilities
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Milad Rezanezhad**

- GitHub: [https://github.com/miladrezanezhad](https://github.com/miladrezanezhad)
- Project: [https://github.com/miladrezanezhad/story-toolkit](https://github.com/miladrezanezhad/story-toolkit)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🌟 Support

If you find this project useful, please consider giving it a ⭐️ on GitHub!

---

*Built with ❤️ for writers and developers*

## ✨ **Version 2.0.0 Highlights**

| Feature | Description |
|---------|-------------|
| 🎯 **Badges** | Python, License, Version, Author shields |
| ⚡ **Quick Start** | Ready-to-run code with sample output |
| 🤖 **LLM Support** | OpenAI, Anthropic, and local models |
| 📁 **Structure** | Project directory layout with new llm/ module |
| 📖 **Docs** | Links to English and Persian documentation |
| 🧪 **Tests** | How to run unit tests including LLM tests |
| 🛠️ **Examples** | Code snippets for each component |
| 🔄 **Upgrade Guide** | How to upgrade from v1 to v2 |
