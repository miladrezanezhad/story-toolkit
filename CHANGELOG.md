# Changelog

All notable changes to the Story Development Toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-05-08

### 🚀 Added
- **LLM Layer** - Optional integration with Large Language Models
  - `LLMFactory` class for creating LLM backends
  - `LLMProvider` enum with support for: OPENAI, ANTHROPIC, LOCAL, MOCK
  - `BaseLLMBackend` abstract base class for custom backends
  - Mock backend for testing without API keys
- **Advanced Dialogue Generation**
  - `use_advanced` parameter in `DialogueGenerator.generate_dialogue()`
  - `style` parameter for dialogue styles: natural, dramatic, poetic, humorous
  - `num_lines` parameter to control dialogue length
- **New StoryToolkit Methods**
  - `get_llm_status()` - Check LLM backend availability
  - `generate_advanced_dialogue()` - Direct access to LLM dialogue generation
- **New DialogueGenerator Methods**
  - `has_llm()` - Check if LLM backend is available
  - `get_llm_info()` - Get information about the configured LLM
- **Installation Options**
  - `pip install story-toolkit[openai]` - OpenAI support
  - `pip install story-toolkit[anthropic]` - Anthropic support
  - `pip install story-toolkit[local]` - Local LLM support (Ollama)
  - `pip install story-toolkit[all]` - All LLM backends

### 🔧 Changed
- **Python Version Requirement** - Minimum version changed from 3.8 to 3.11
- **StoryToolkit Constructor** - Added optional `llm_backend` parameter
- **DialogueGenerator Constructor** - Added optional `llm_backend` parameter
- **generate_full_story** - Added `use_advanced_dialogue` parameter
- **generate_monologue** - Added `use_advanced` parameter
- **create_conversation_scene** - Added `use_advanced` parameter
- **Documentation** - Complete rewrite for v2.0.0 with LLM examples

### ✅ Fixed
- All tests now pass with 100% success rate (16/16 tests)
- Improved error handling for LLM backend failures
- Better fallback to template dialogue when LLM fails

### 🔄 Deprecated
- Nothing deprecated. All v1.0.0 code continues to work unchanged.

### 🗑️ Removed
- Nothing removed. Full backward compatibility maintained.

---

## [1.0.0] - 2026-05-07

### 🚀 Added
- Initial release of Story Development Toolkit
- **Core Modules**
  - `StoryEngine` - Main story creation and management engine
  - `Character` - Character creation with traits, goals, skills, fears, relationships
  - `Plot` - Plot structure management with plot points and subplots
  - `WorldBuilder` - World building with locations, cultures, rules, factions
- **Generators**
  - `CharacterGenerator` - Random character generation
  - `PlotGenerator` - Plot generation for multiple genres
  - `DialogueGenerator` - Template-based dialogue generation
- **NLP Tools**
  - `CoherenceChecker` - Story coherence analysis
  - `TextAnalyzer` - Readability and text analysis
- **Utility Functions**
  - `save_story()` - Save story to JSON
  - `load_story()` - Load story from JSON
  - `export_to_markdown()` - Export story to Markdown
- **Documentation**
  - English documentation (Quick Start, API Reference)
  - Persian documentation (مستندات فارسی)
  - 18+ unit tests

### 🔧 Changed
- N/A (initial release)

### ✅ Fixed
- N/A (initial release)

---

## [Unreleased]

### 🔜 Planned for v2.1.0
- Long-term memory with SQLite backend
- Export to EPUB and PDF formats
- CLI tool for command-line usage
- Pre-built story templates

### 🔮 Planned for v3.0.0
- Vector database support for semantic search
- Real-time story timeline visualization
- Plugin system for custom extensions
- Web-based story editor

---

## Upgrade Guide

### From v1.0.0 to v2.0.0

**No breaking changes!** Your existing v1.0.0 code will continue to work exactly as before.

```python
# This v1.0.0 code still works perfectly
from story_toolkit import StoryToolkit

toolkit = StoryToolkit()
story = toolkit.create_story("fantasy", "courage")
# ... everything works as before
```

To use new LLM features:

```python
# Optional: Add LLM for enhanced capabilities
from story_toolkit.llm import LLMFactory, LLMProvider

llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# Now you can use advanced dialogue
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Hero", "Villain",
    use_advanced=True,
    style="dramatic"
)
```

---

## Version History

| Version | Release Date | Python Support | Status |
|---------|--------------|----------------|--------|
| 2.0.0 | 2026-05-08 | 3.11+ | ✅ Current |
| 1.0.0 | 2026-05-07 | 3.8+ | ✅ Stable |

---

## Links

- [Full Documentation](https://miladrezanezhad.github.io/story-toolkit/)
- [GitHub Repository](https://github.com/miladrezanezhad/story-toolkit)
- [Issue Tracker](https://github.com/miladrezanezhad/story-toolkit/issues)
- [PyPI Package](https://pypi.org/project/story-toolkit/)
