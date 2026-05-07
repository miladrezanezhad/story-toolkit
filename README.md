

```markdown
# 📚 Story Development Toolkit
```
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/miladrezanezhad/story-toolkit)
[![Author](https://img.shields.io/badge/Author-Milad%20Rezanezhad-purple.svg)](https://github.com/miladrezanezhad)

**A comprehensive Python toolkit for generating engaging and coherent stories.**

Story Development Toolkit provides tools for character creation, plot generation, dialogue writing, world building, and story coherence analysis — all in one package.

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

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/miladrezanezhad/story-toolkit.git
cd story-toolkit

# Install dependencies
pip install -r requirements.txt

# Or install as editable package
pip install -e .
```

---

## 🚀 Quick Start

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

# Generate dialogue
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

---

## 📁 Project Structure

```
story_toolkit/
├── story_toolkit/          # Main Python package
│   ├── core/               # Story engine, Character, Plot, WorldBuilder
│   ├── generators/         # Character, Plot, and Dialogue generators
│   ├── nlp/                # Coherence checker and Text analyzer
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

Or open the language selection page:

```bash
start docs/index.html
```

### Documentation Pages

- **Quick Start Guide** — Build your first story in 5 minutes
- **API Reference** — Complete documentation for all classes and methods
- **Examples** — Simple, complete, and advanced usage examples

---

## 🧪 Running Tests

```bash
# Core module tests
python -m tests.test_core

# Generator tests
python -m tests.test_generators

# NLP tool tests
python -m tests.test_nlp
```

All tests should pass:
```
✅ StoryEngine tests passed!
✅ Character tests passed!
✅ Plot tests passed!
✅ WorldBuilder tests passed!
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

### Advanced Features
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

---

## 🔧 Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`:
  - `nltk>=3.8.1`
  - `spacy>=3.7.0`
  - `textblob>=0.17.1`
  - `pydantic>=2.5.0`
  - `pyyaml>=6.0`

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


## ✨ **README Features:**



| Section | Description |
|---------|-------------|
| 🎯 **Badges** | Python, License, Version, Author shields |
| ⚡ **Quick Start** | Ready-to-run code with sample output |
| 📁 **Structure** | Project directory layout |
| 📖 **Docs** | Links to English and Persian documentation |
| 🧪 **Tests** | How to run unit tests |
| 🛠️ **Examples** | Code snippets for each component |
| 🤝 **Contributing** | Guide for contributors |


