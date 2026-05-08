
# Changelog

All notable changes to the Story Development Toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.2] - 2026-05-08

### 🚀 Added
- **CLI Tool** - Full command-line interface
  - `story new --genre --theme` - Create new stories
  - `template list` - List all available templates
  - `template use <name>` - Apply pre-built templates
  - `story list` - List stories in memory
- **Batch Story Generation** - Create multiple stories at once
- **Story Preview** - Display story preview before export

### 🔧 Changed
- Improved CLI error handling and user feedback
- Enhanced command-line argument parsing
- Better help messages and documentation

### ✅ Fixed
- CLI command execution in all environments
- Path handling for cross-platform compatibility
- Output file naming conventions

---

## [2.2.1] - 2026-05-08

### 🚀 Added
- **5 Pre-built Story Templates**
  - `hero_journey` - 12-stage Campbell's monomyth
  - `three_act` - 3-act structure (Setup, Confrontation, Resolution)
  - `mystery_clues` - 5-stage detective/mystery structure
  - `romance_beat` - 15-beat romance structure
  - `horror_cycle` - 6-stage horror structure
- **TemplateManager Class** - Full API for template management
- **Template Integration** - `use_template()`, `list_templates()`, `get_template_info()`

### 🔧 Changed
- Updated `StoryToolkit` to support template methods
- Enhanced template documentation

### ✅ Fixed
- Template stage extraction and naming consistency

---

## [2.2.0] - 2026-05-08

### 🚀 Added
- **EPUB Exporter** - Export stories as eBooks (compatible with Amazon, Kobo, Apple Books)
- **PDF Exporter** - Three PDF styles:
  - `PRINT` - Standard print format
  - `MANUSCRIPT` - Publisher submission format
  - `EBOOK` - Screen reading format
- **HTML Exporter** - Four HTML templates:
  - `MODERN` - Responsive design
  - `CLASSIC` - Book-style with dropcaps
  - `DARK` - Night reading mode
  - `MINIMAL` - Clean and lightweight
- **Bionic Reading Converter** - Enhanced readability by bolding first letters
  - `to_bionic()` function
  - Configurable strength (1-3 letters)
  - HTML output with `<strong>` tags

### 🔧 Changed
- Exporters module structure and organization
- Improved PDF content rendering

### ✅ Fixed
- PDF content display issues
- HTML template responsiveness

---

## [2.1.0] - 2026-05-08

### 🚀 Added
- **Long-term Memory with SQLite**
  - `MemoryManager` class for persistent storage
  - `SQLiteMemory` backend implementation
  - Story save/load functionality
  - Timeline events management
  - Character storage and retrieval
  - Event search by keyword
  - Story statistics
  - Consistency checking

### 🔧 Changed
- Updated `StoryToolkit` to support memory backend
- Added `save_to_memory` parameter to `create_story()`
- Added `add_event()` and `get_timeline()` methods

### ✅ Fixed
- Duplicate character prevention in memory
- Timeline event ordering

---

## [2.0.0] - 2026-05-07

### 🚀 Added
- **LLM Layer** - Optional integration with Large Language Models
  - `LLMProvider` enum with support for: OPENAI, ANTHROPIC, LOCAL, MOCK
  - `LLMFactory` for creating LLM backends
  - `BaseLLMBackend` abstract base class
  - Mock backend for testing (no API key required)
- **Advanced Dialogue Generation**
  - `use_advanced` parameter in `generate_dialogue()`
  - `style` parameter for dialogue styles: natural, dramatic, poetic, humorous
  - `num_lines` parameter for dialogue length control
- **New StoryToolkit Methods**
  - `get_llm_status()` - Check LLM availability
  - `generate_advanced_dialogue()` - Direct LLM dialogue generation
- **New DialogueGenerator Methods**
  - `has_llm()` - Check if LLM is available
  - `get_llm_info()` - Get LLM configuration

### 🔧 Changed
- **Python Version Requirement** - Minimum version changed from 3.8 to **3.11+**
- `StoryToolkit.__init__()` - Added optional `llm_backend` parameter
- `DialogueGenerator.__init__()` - Added optional `llm_backend` parameter
- `generate_full_story()` - Added `use_advanced_dialogue` parameter

### ✅ Fixed
- All tests pass with 100% success rate
- Improved error handling for LLM failures
- Better fallback to template dialogue

### 🔄 Deprecated
- Nothing deprecated. All v1.0.0 code continues to work unchanged.

---

## [1.0.0] - 2026-05-07

### 🚀 Added
- **Initial Release** - Core features
- **Core Modules**
  - `StoryEngine` - Main story creation engine
  - `Character` - Character creation with traits, goals, skills, fears, relationships
  - `Plot` - Plot structure with points and subplots
  - `WorldBuilder` - World building with locations, cultures, rules, factions
- **Generators**
  - `CharacterGenerator` - Random character generation
  - `PlotGenerator` - Genre-based plot generation
  - `DialogueGenerator` - Template-based dialogue generation
- **NLP Tools**
  - `CoherenceChecker` - Story coherence analysis
  - `TextAnalyzer` - Readability and text analysis
- **Utility Functions**
  - `save_story()` / `load_story()` - JSON storage
  - `export_to_markdown()` - Markdown export
- **Documentation**
  - English documentation (Quick Start, API Reference)
  - Persian documentation (مستندات فارسی)
- **Testing**
  - 16+ unit tests (100% pass rate)

---

## [Unreleased]

### 🔜 Planned for v2.3.0
- GUI Desktop Application (Tkinter/PyQt)
- VS Code Extension
- Obsidian Plugin
- Cloud API (optional)

### 🔮 Planned for v3.0.0
- Vector database for semantic search (ChromaDB/FAISS)
- Real-time collaboration
- Web-based story editor

---

## Upgrade Guide

### From v1.0.0 to v2.0.0

**No breaking changes!** Your existing v1.0.0 code works unchanged.

```python
# This v1.0.0 code still works perfectly
from story_toolkit import StoryToolkit

toolkit = StoryToolkit()
story = toolkit.create_story("fantasy", "courage")
# ... everything works as before
```

### From v2.0.0 to v2.1.0

```python
# Optional: Add memory for persistent storage
toolkit = StoryToolkit(memory_backend="sqlite", db_path="stories.db")
story = toolkit.create_story("fantasy", "courage", save_to_memory=True)
```

### From v2.1.0 to v2.2.0

```python
# Optional: Export to different formats
from story_toolkit.exporters import PDFExporter, ExportConfig

config = ExportConfig(title="My Story", author="Me")
exporter = PDFExporter(config)
exporter.export(story, "my_story.pdf")
```

### From v2.2.0 to v2.2.1

```python
# New: Use pre-built templates
story = toolkit.use_template("hero_journey", genre="fantasy")
```

### From v2.2.1 to v2.2.2

```bash
# New: CLI tool
story-toolkit story new --genre fantasy --theme courage
story-toolkit template list
story-toolkit template use hero_journey
```

---

## Version History

| Version | Release Date | Python Support | Status |
|---------|--------------|----------------|--------|
| **2.2.2** | 2026-05-08 | **3.11+** | ✅ Current |
| 2.2.1 | 2026-05-08 | 3.11+ | ✅ Stable |
| 2.2.0 | 2026-05-08 | 3.11+ | ✅ Stable |
| 2.1.0 | 2026-05-08 | 3.11+ | ✅ Stable |
| 2.0.0 | 2026-05-07 | 3.11+ | ✅ Stable |
| 1.0.0 | 2026-05-07 | 3.8+ | ✅ Stable |

---

## Links

- [Full Documentation](https://miladrezanezhad.github.io/story-toolkit/)
- [GitHub Repository](https://github.com/miladrezanezhad/story-toolkit)
- [Issue Tracker](https://github.com/miladrezanezhad/story-toolkit/issues)
- [PyPI Package](https://pypi.org/project/story-toolkit/)

---

*Maintained with ❤️ by Milad Rezanezhad*
