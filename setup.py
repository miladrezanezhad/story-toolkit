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
    version="1.0.0",
    author="Milad Rezanezhad",
    author_email="milad.rezanezhad@example.com",
    description="A comprehensive toolkit for generating engaging and coherent stories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miladrezanezhad/story-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "story-toolkit=story_toolkit.cli:main",
        ],
    },
)
