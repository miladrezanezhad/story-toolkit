## 📄 **CONTRIBUTING.md**

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

### 💡 Suggesting Features

Feature suggestions are welcome! Please:
1. Check existing issues to avoid duplicates
2. Open a new issue with the "enhancement" label
3. Describe the feature and why it would be useful

### 📝 Improving Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add more examples
- Translate to new languages
- Improve API documentation

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

### Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Install in Development Mode

```bash
pip install -e .
```

### Run Tests

```bash
# All tests
python -m tests.test_core
python -m tests.test_generators
python -m tests.test_nlp
```

---

## Coding Guidelines

### Python Version
- Target Python 3.11 or higher

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
        
    Raises:
        ValueError: If trait is empty.
    """
    ...
```

### Imports
Order imports as follows:
1. Standard library
2. Third-party packages
3. Local imports

```python
import os
from typing import List, Dict

import nltk

from story_toolkit.core.character import Character
```

### Naming Conventions
- Classes: `PascalCase` → `CharacterGenerator`
- Functions: `snake_case` → `generate_character()`
- Variables: `snake_case` → `character_name`
- Constants: `UPPER_SNAKE_CASE` → `MAX_CHARACTERS`

---

## Testing

### Writing Tests

- Every new feature should include tests
- Bug fixes should include a regression test
- Aim for clear, readable test names

```python
def test_character_creation():
    """Test basic character creation."""
    char = Character(name="Test", age=25, role="protagonist")
    assert char.name == "Test"
    assert char.age == 25
```

### Running Tests

```bash
# Run specific test file
python -m tests.test_core

# Run all tests
python -m tests.test_core && python -m tests.test_generators && python -m tests.test_nlp
```

---

## Pull Request Process

### Before Submitting

1. ✅ Run all tests and make sure they pass
2. ✅ Update documentation if needed
3. ✅ Add your changes to the CHANGELOG (if exists)
4. ✅ Write clear commit messages

### Commit Messages

Follow conventional commits:

```
feat: Add new character arc system
fix: Fix plot point connection bug
docs: Update API documentation
test: Add tests for world builder
refactor: Simplify dialogue generator
```

### Submitting

1. Push to your fork
2. Open a Pull Request to the `main` branch
3. Fill in the PR template
4. Link any related issues

### Pull Request Template

Your PR description should include:

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] All tests pass
- [ ] New tests added

## Screenshots (if applicable)
```

### Review Process

- Maintainers will review within 48 hours
- Address review comments
- Use the "Request Changes" and "Approve" flow
- Once approved, a maintainer will merge

---

## Style Guide

### Project Structure

```
story_toolkit/
├── core/           # Core modules
├── generators/     # Content generators
├── nlp/            # NLP tools
└── utils/          # Utilities
```

### Adding New Modules

1. Place in the appropriate package
2. Add `__init__.py` with proper exports
3. Register in the main `__init__.py`
4. Add tests in `tests/`
5. Update documentation

---

## 📖 Documentation

### Code Documentation
- Document all public methods and classes
- Include usage examples
- Keep documentation up to date

### Wiki Contributions
- Wiki pages can be edited by anyone
- Follow the existing format
- Keep information accurate and helpful

---

## 🎯 Priorities

Not sure what to work on? Here are current priorities:

1. 🐛 Bug fixes
2. 📝 Documentation improvements
3. 🧪 Adding more tests
4. ✨ New genre support
5. 🌍 Translations

---

## 📞 Getting Help

Need help? Here's how to reach out:

- **Questions:** [GitHub Discussions](https://github.com/miladrezanezhad/story-toolkit/discussions)
- **Bugs:** [GitHub Issues](https://github.com/miladrezanezhad/story-toolkit/issues)
- **Email:** Open an issue for private contact

---

## 🏆 Recognition

All contributors will be recognized in the [README](README.md) and release notes.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*Happy contributing! 🚀*
