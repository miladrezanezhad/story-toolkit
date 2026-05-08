
# 🤝 Contributing to Story Development Toolkit

First off, thank you for considering contributing! 🎉

This document provides guidelines for contributing to Story Development Toolkit.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating a bug report:
1. Check the [Issues](https://github.com/miladrezanezhad/story-toolkit/issues) page
2. Make sure the bug hasn't been reported before
3. Use the bug report template

**A good bug report includes:**
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages and screenshots
- Story Toolkit version

### 💡 Suggesting Features

Feature suggestions are welcome! Please:
1. Check existing issues to avoid duplicates
2. Open a new issue with the "enhancement" label
3. Describe the feature and why it would be useful
4. Indicate which version you'd like to see it in (v2.x.x)

**Current priority features:**
- More LLM backends (Google Gemini, Cohere)
- Export to additional formats (DOCX, TXT)
- Web-based editor
- Real-time collaboration

### 📝 Improving Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add more examples
- Translate to new languages
- Improve API documentation
- Update wiki pages

### 💻 Writing Code

Ready to code? Great! Here's what you can work on:
- Open issues labeled "good first issue"
- Bug fixes
- New features
- Adding tests
- Performance improvements

---

## Getting Started

### 1. Fork the Repository

Click the **Fork** button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/story-toolkit.git
cd story-toolkit
```

### 3. Add Upstream Remote

```bash
git remote add upstream https://github.com/miladrezanezhad/story-toolkit.git
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

---

## Development Setup

### Requirements

- Python 3.11 or higher
- pip (latest version)

### Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (testing, linting)
pip install -r requirements-dev.txt

# Optional LLM dependencies
pip install -r requirements-llm.txt

# Optional export dependencies
pip install -r requirements-export.txt

# Install in development mode
pip install -e .
```

### Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

---

## Project Structure (v2.2.2)

```
story_toolkit/
├── core/           # Core modules (Character, Plot, WorldBuilder)
├── generators/     # Content generators (Character, Plot, Dialogue, Story)
├── nlp/            # NLP tools (CoherenceChecker, TextAnalyzer)
├── llm/            # LLM integration (v2.0.0)
├── memory/         # SQLite memory (v2.1.0)
├── exporters/      # PDF, EPUB, HTML, Bionic (v2.2.0)
├── templates/      # Pre-built story templates (v2.2.1)
├── cli/            # Command-line interface (v2.2.2)
└── utils/          # Helper functions
```

---

## Coding Guidelines

### Python Version
- Target Python **3.11 or higher**

### Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names

### Type Hints
Always use type hints:

```python
def create_story(genre: str, theme: str, complexity: int = 3) -> dict:
    """Create a new story."""
    ...
```

### Docstrings
Use Google-style docstrings:

```python
def add_trait(self, trait: str) -> None:
    """Add a personality trait to the character.
    
    Args:
        trait: The personality trait to add.
        
    Returns:
        None
        
    Raises:
        ValueError: If trait is empty.
        
    Example:
        >>> hero.add_trait("brave")
    """
    if not trait:
        raise ValueError("Trait cannot be empty")
    self._traits.append(trait)
```

### Imports
Order imports as follows:
1. Standard library
2. Third-party packages
3. Local imports

```python
import os
from typing import List, Dict, Optional

import nltk
from pydantic import BaseModel

from story_toolkit.core.character import Character
from story_toolkit.utils.helpers import save_story
```

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Classes | `PascalCase` | `CharacterGenerator` |
| Functions | `snake_case` | `generate_character()` |
| Variables | `snake_case` | `character_name` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_CHARACTERS` |
| Private methods | `_leading_underscore` | `_validate_input()` |

---

## Testing

### Writing Tests

- Every new feature should include tests
- Bug fixes should include a regression test
- Aim for clear, readable test names

```python
def test_character_creation():
    """Test basic character creation."""
    # Setup
    char = Character(name="Test", age=25, role="protagonist")
    
    # Assertions
    assert char.name == "Test"
    assert char.age == 25
    assert char.role == "protagonist"
```

### Test Structure by Version

| Version | Test Location |
|---------|---------------|
| v1.0.0 | `tests/test_core.py` |
| v2.0.0 | `tests/test_llm.py`, `tests/test_llm_quick/` |
| v2.1.0 | `tests/v2_1/test_memory.py` |
| v2.2.0 | `tests/v2_2/test_exporters.py` |
| v2.2.1 | `tests/v2_2_1/test_templates.py` |
| v2.2.2 | `tests/v2_2_2/test_cli.py` |

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
python -m tests.test_core
python tests/v2_2_2/test_cli.py

# Run with coverage
pytest tests/ --cov=story_toolkit --cov-report=html
```

---

## Pull Request Process

### Before Submitting

1. ✅ Run all tests and make sure they pass
2. ✅ Update documentation if needed
3. ✅ Add your changes to `CHANGELOG.md`
4. ✅ Write clear commit messages
5. ✅ Ensure backward compatibility with v1.0.0

### Commit Messages

Follow conventional commits:

```
feat: Add new character arc system
fix: Fix plot point connection bug
docs: Update API documentation for v2.2.2
test: Add tests for CLI tool
refactor: Simplify dialogue generator
chore: Update dependencies
```

### Commit Message Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Submitting

1. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request to the `main` branch
3. Fill in the PR template
4. Link any related issues

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Breaking change

## Version Impact
- [ ] v1.0.0 compatible
- [ ] v2.0.0 compatible
- [ ] v2.1.0 compatible
- [ ] v2.2.0 compatible
- [ ] v2.2.1 compatible
- [ ] v2.2.2 compatible

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Screenshots (if applicable)
```

### Review Process

- Maintainers will review within 48 hours
- Address review comments
- Use the "Request Changes" and "Approve" flow
- Once approved, a maintainer will merge

---

## Style Guide

### Project Structure Rules

- Core modules go in `core/` (v1.0.0)
- Generators go in `generators/` (v1.0.0)
- New features should have their own module
- Each version's features should be isolated
- Maintain backward compatibility

### Adding New Features

1. Create new module folder (e.g., `exporters/`, `templates/`)
2. Add `__init__.py` with proper exports
3. Register in main `__init__.py`
4. Add tests in appropriate test folder
5. Update `CHANGELOG.md`
6. Update documentation

### Code Quality Tools

```bash
# Format code
black story_toolkit/ tests/ --line-length 100

# Sort imports
isort story_toolkit/ tests/ --profile black

# Lint code
flake8 story_toolkit/ --max-line-length=100 --ignore=E203,W503

# Type checking
mypy story_toolkit/ --ignore-missing-imports
```

---

## 📖 Documentation

### Code Documentation
- Document all public methods and classes
- Include usage examples
- Keep documentation up to date with version changes
- Mention which version introduced each feature

### Wiki Contributions
- Wiki pages can be edited by anyone
- Follow the existing format
- Keep information accurate and helpful
- Update version numbers when applicable

### API Documentation
- Update `docs/eng/api.html` and `docs/fa-ir/api.html`
- Include examples for all methods
- Show version information for features

---

## 🎯 Current Priorities

| Priority | Area | Difficulty |
|----------|------|------------|
| 🔥 High | Bug fixes | Easy |
| 🔥 High | Documentation | Easy |
| 🔥 High | Test coverage | Medium |
| ⭐ Medium | More LLM backends | Hard |
| ⭐ Medium | Export formats | Medium |
| 💡 Low | GUI application | Hard |
| 💡 Low | Web editor | Hard |

---

## 📞 Getting Help

Need help? Here's how to reach out:

- **Questions:** [GitHub Discussions](https://github.com/miladrezanezhad/story-toolkit/discussions)
- **Bugs:** [GitHub Issues](https://github.com/miladrezanezhad/story-toolkit/issues)
- **Discord:** (coming soon)
- **Email:** Open an issue for private contact

---

## 🏆 Recognition

All contributors will be recognized in:
- [README.md](README.md) contributors list
- Release notes
- GitHub Hall of Fame

**Current Contributors:**
- Milad Rezanezhad (Creator & Maintainer)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*Happy contributing! 🚀*
