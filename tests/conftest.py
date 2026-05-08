"""
Pytest configuration and shared fixtures for story-toolkit tests.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import pytest
import json
import os
from pathlib import Path

# Fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_story():
    """Create a sample story for testing"""
    from story_toolkit import StoryToolkit
    
    toolkit = StoryToolkit()
    story = toolkit.create_story(genre="fantasy", theme="courage")
    return story

@pytest.fixture
def sample_characters():
    """Create sample characters for testing"""
    from story_toolkit.core.character import Character
    
    hero = Character(name="Aria", age=25, role="protagonist")
    hero.add_trait("brave")
    hero.add_trait("compassionate")
    hero.add_skill("sword_mastery")
    
    villain = Character(name="Malakor", age=50, role="antagonist")
    villain.add_trait("cunning")
    villain.add_trait("ruthless")
    
    mentor = Character(name="Old Ben", age=70, role="mentor")
    mentor.add_trait("wise")
    
    return [hero, villain, mentor]

@pytest.fixture
def sample_world():
    """Create a sample world for testing"""
    from story_toolkit.core.world_builder import WorldBuilder
    
    builder = WorldBuilder()
    world = builder.create_world("Eldoria", "fantasy")
    world.add_location("Crystal City", "Ancient metropolis", "city")
    world.add_rule("magic", "Only pure hearts can use magic")
    
    return world

@pytest.fixture
def mock_llm_backend():
    """Create a mock LLM backend for testing"""
    from story_toolkit.llm import LLMFactory, LLMProvider
    
    return LLMFactory.create_backend(provider=LLMProvider.MOCK)

@pytest.fixture
def toolkit_with_llm(mock_llm_backend):
    """Create StoryToolkit with mock LLM"""
    from story_toolkit import StoryToolkit
    
    return StoryToolkit(llm_backend=mock_llm_backend)

@pytest.fixture
def sample_story_data():
    """Load sample story data from fixture file"""
    fixture_file = FIXTURES_DIR / "sample_story.json"
    if fixture_file.exists():
        with open(fixture_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None