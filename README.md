
# 📚 Story Development Toolkit

[![Tests](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.2.2-orange.svg)](https://github.com/miladrezanezhad/story-toolkit/releases)
[![Author](https://img.shields.io/badge/Author-Milad%20Rezanezhad-purple.svg)](https://github.com/miladrezanezhad)
[![PyPI version](https://img.shields.io/pypi/v/story-toolkit.svg)](https://pypi.org/project/story-toolkit/)

**A comprehensive Python toolkit for generating engaging and coherent stories with optional LLM support.**

Story Development Toolkit provides tools for character creation, plot generation, dialogue writing, world building, and story coherence analysis — all in one package. **NEW in v2.2.2:** Complete CLI tool and pre-built story templates!

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
| 🤖 **LLM Support** | Optional integration with OpenAI, Anthropic, and local models |
| 💾 **Long-term Memory** | SQLite database for story persistence (v2.1.0) |
| 📄 **Export Formats** | PDF, EPUB, HTML, JSON, Markdown (v2.2.0) |
| 📋 **Pre-built Templates** | Hero's Journey, 3-Act, Mystery, Romance, Horror (v2.2.1) |
| 💻 **CLI Tool** | Command-line interface for easy usage (v2.2.2) |

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

# With export formats (PDF, EPUB)
pip install story-toolkit[export]

# Full installation (all features)
pip install story-toolkit[all]

# Or install from source
git clone https://github.com/miladrezanezhad/story-toolkit.git
cd story-toolkit
pip install -e .
```

---

## 🚀 Quick Start

### Basic Usage (No LLM)

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

### Using Pre-built Templates (v2.2.1)

```python
from story_toolkit import StoryToolkit

toolkit = StoryToolkit()

# Create story using Hero's Journey template (12 stages)
story = toolkit.use_template("hero_journey", genre="fantasy", theme="redemption")

# List all available templates
templates = toolkit.list_templates()
for t in templates:
    print(f"{t['name']}: {t['stage_count']} stages")
```

### Export to PDF (v2.2.0)

```python
from story_toolkit import StoryToolkit
from story_toolkit.exporters import PDFExporter, ExportConfig, PDFStyle

toolkit = StoryToolkit()
story = toolkit.create_story("fantasy", "courage")

# Export as PDF
config = ExportConfig(title="My Story", author="Me", pdf_style=PDFStyle.PRINT)
exporter = PDFExporter(config)
exporter.export(story, "my_story.pdf")
```

### Using CLI Tool (v2.2.2)

```bash
# Create a new story
story-toolkit story new --genre fantasy --theme courage

# List available templates
story-toolkit template list

# Use a template
story-toolkit template use hero_journey --output my_story.json
```

### Advanced Usage with LLM

```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# Create LLM backend (Mock for testing)
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# Generate advanced dialogue
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Kai", "Villain",
    context="final_battle",
    use_advanced=True,
    style="dramatic",
    num_lines=8
)

# Check LLM status
print(f"LLM Status: {toolkit.get_llm_status()}")
```

---

## 🤖 LLM Backends

v2.0.0+ supports multiple LLM providers:

| Provider | Installation | API Key Required |
|----------|--------------|------------------|
| **Mock** | Included | ❌ No (for testing) |
| **OpenAI** | `pip install story-toolkit[openai]` | ✅ Yes |
| **Anthropic** | `pip install story-toolkit[anthropic]` | ✅ Yes |
| **Local (Ollama)** | `pip install story-toolkit[local]` | ❌ No (free) |

---

## 📋 Pre-built Templates (v2.2.1)

| Template Name | Genre | Stages | Description |
|---------------|-------|--------|-------------|
| `hero_journey` | Fantasy/Adventure | 12 | Campbell's monomyth |
| `three_act` | General | 3 | Standard 3-act structure |
| `mystery_clues` | Mystery | 5 | Detective story structure |
| `romance_beat` | Romance | 15 | 15-beat romance structure |
| `horror_cycle` | Horror | 6 | Classic horror structure |

---

## 📄 Export Formats (v2.2.0)

| Format | Description | Usage |
|--------|-------------|-------|
| **PDF** | Print, Manuscript, eBook styles | `exporter.export(story, "file.pdf")` |
| **EPUB** | eBook for Amazon/Kobo/Apple | `exporter.export(story, "file.epub")` |
| **HTML** | 4 templates (Modern, Classic, Dark, Minimal) | `exporter.export(story, "file.html")` |
| **JSON** | Raw data | `save_story(story, "file.json")` |
| **Markdown** | Readable text | `export_to_markdown(story, "file.md")` |

---

## 💾 Memory Storage (v2.1.0)

```python
from story_toolkit import StoryToolkit

# Enable SQLite memory
toolkit = StoryToolkit(memory_backend="sqlite", db_path="stories.db")

# Create story with auto-save
story = toolkit.create_story("fantasy", "courage", save_to_memory=True)

# Add events to timeline
toolkit.add_event(1, "Hero discovers the map", "plot", 9)

# View timeline
for event in toolkit.get_timeline():
    print(f"Chapter {event.chapter}: {event.description}")

# List all saved stories
stories = toolkit.list_stored_stories()
```

---

## 📁 Project Structure

```
story_toolkit/
├── story_toolkit/          # Main Python package
│   ├── core/               # Story engine, Character, Plot, WorldBuilder
│   ├── generators/         # Character, Plot, Dialogue, Story generators
│   ├── nlp/                # Coherence checker and Text analyzer
│   ├── llm/                # LLM layer (OpenAI, Anthropic, Local, Mock)
│   ├── memory/             # SQLite long-term memory
│   ├── exporters/          # PDF, EPUB, HTML, Bionic exporters
│   ├── templates/          # Pre-built story templates
│   ├── cli/                # Command-line interface
│   └── utils/              # Helper functions
├── docs/                   # Documentation (English & Persian)
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
- **CLI Guide** — Command-line interface usage
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

# Comprehensive test suite
python tests/test_suite.py
```

All tests should pass:
```
✅ StoryEngine tests passed!
✅ Character tests passed!
✅ Plot tests passed!
✅ WorldBuilder tests passed!
✅ LLM layer tests passed!
✅ Memory tests passed!
✅ Exporter tests passed!
✅ CLI tests passed!
```

---

## 🎮 Usage Examples

```bash
# Simple example
python -m examples.simple_example

# Complete demo
python -m examples.example

# Advanced features (with LLM)
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

- Python 3.11 or higher
- Dependencies listed in `requirements.txt`:
  - `nltk>=3.8.1`
  - `spacy>=3.7.0`
  - `textblob>=0.17.1`
  - `pydantic>=2.5.0`
  - `pyyaml>=6.0`

### Optional Dependencies

| Backend/Feature | Package |
|-----------------|---------|
| OpenAI | `openai>=1.0.0` |
| Anthropic | `anthropic>=0.18.0` |
| Local LLM | `ollama>=0.1.0` |
| PDF Export | `reportlab>=4.0` |
| EPUB Export | `ebooklib>=0.18` |

---

## 🔄 Version History

| Version | Features | Python |
|---------|----------|--------|
| **2.2.2** | CLI Tool, Complete integration | 3.11+ |
| 2.2.1 | Pre-built Templates (5 templates) | 3.11+ |
| 2.2.0 | Exporters (PDF, EPUB, HTML, Bionic) | 3.11+ |
| 2.1.0 | SQLite Memory, Timeline, Storage | 3.11+ |
| 2.0.0 | LLM Layer (OpenAI, Anthropic, Local) | 3.11+ |
| 1.0.0 | Core Features (Character, Plot, World) | 3.8+ |

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

---

## ✨ **Version 2.2.2 Highlights**

| Feature | Description |
|---------|-------------|
| 🎯 **Badges** | Python 3.11+, License, Version 2.2.2, Author |
| 🤖 **LLM Support** | OpenAI, Anthropic, Local (Ollama) |
| 💾 **Memory** | SQLite long-term persistence |
| 📄 **Exporters** | PDF, EPUB, HTML (4 templates), Bionic Reading |
| 📋 **Templates** | 5 pre-built story structures |
| 💻 **CLI Tool** | Full command-line interface |
| 📖 **Docs** | English & Persian documentation |
| 🧪 **Tests** | 100% pass rate (16+ tests) |
| 🔄 **Backward Compatible** | v1.0.0 code works unchanged |
