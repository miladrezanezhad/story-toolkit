"""
Setup configuration for Story Development Toolkit.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="story-toolkit",
    version="2.0.0",
    author="Milad Rezanezhad",
    author_email="milad.rezanezhad@example.com",
    description="A comprehensive toolkit for generating engaging and coherent stories with optional LLM support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miladrezanezhad/story-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "nltk>=3.8.1",
        "spacy>=3.7.0",
        "textblob>=0.17.1",
        "pydantic>=2.5.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        # LLM backends
        "openai": [
            "openai>=1.0.0",
        ],
        "anthropic": [
            "anthropic>=0.18.0",
        ],
        "local": [
            "ollama>=0.1.0",
        ],
        "llama-cpp": [
            "llama-cpp-python>=0.2.0",
        ],
        # Complete LLM support (all backends)
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
            "ollama>=0.1.0",
        ],
        # Development dependencies
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "types-pyyaml>=6.0.0",
            "types-requests>=2.31.0",
        ],
        # Documentation
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        # Testing
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.11.0",
        ],
        # Complete installation (all optional dependencies)
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
            "ollama>=0.1.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "story-toolkit=story_toolkit.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/miladrezanezhad/story-toolkit/issues",
        "Source": "https://github.com/miladrezanezhad/story-toolkit",
        "Documentation": "https://miladrezanezhad.github.io/story-toolkit/",
        "Changelog": "https://github.com/miladrezanezhad/story-toolkit/releases",
    },
    keywords=[
        "story", "writing", "narrative", "dialogue", "character",
        "plot", "world-building", "nlp", "creative-writing",
        "fiction", "story-generator", "llm", "openai", "claude",
        "story-telling", "python", "toolkit"
    ],
    include_package_data=True,
    zip_safe=False,
)
