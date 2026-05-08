"""
Tests for LLM layer (new feature)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import pytest
from story_toolkit.llm import LLMFactory, LLMProvider, LLMConfig
from story_toolkit.llm.backends.mock_backend import MockLLMBackend
from story_toolkit import StoryToolkit


class TestLLMFactory:
    """Test LLMFactory class"""
    
    def test_create_mock_backend(self):
        """Test creating mock backend"""
        llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
        
        assert llm is not None
        assert isinstance(llm, MockLLMBackend)
    
    def test_create_backend_with_config(self):
        """Test creating backend with custom config"""
        llm = LLMFactory.create_backend(
            provider=LLMProvider.MOCK,
            temperature=0.5,
            model="custom-model"
        )
        
        assert llm.config.temperature == 0.5
        assert llm.config.model == "custom-model"
    
    def test_create_from_env_mock(self):
        """Test creating backend from environment (mock fallback)"""
        import os
        # Remove any API keys from environment for this test
        os.environ.pop('OPENAI_API_KEY', None)
        os.environ['STORY_LLM_PROVIDER'] = 'mock'
        
        llm = LLMFactory.create_from_env()
        assert llm is not None


class TestMockLLMBackend:
    """Test MockLLMBackend functionality"""
    
    def test_generate(self):
        """Test generate method"""
        llm = MockLLMBackend(LLMConfig(provider=LLMProvider.MOCK))
        response = llm.generate("Hello, world!")
        
        assert response is not None
        assert isinstance(response, str)
    
    def test_generate_dialogue(self):
        """Test dialogue generation with mock"""
        llm = MockLLMBackend(LLMConfig(provider=LLMProvider.MOCK))
        dialogue = llm.generate_dialogue("Hero", "Villain", "conflict")
        
        assert isinstance(dialogue, list)
        assert len(dialogue) > 0
        assert any("Hero" in line for line in dialogue)
    
    def test_generate_dialogue_different_contexts(self):
        """Test dialogue generation with different contexts"""
        llm = MockLLMBackend(LLMConfig(provider=LLMProvider.MOCK))
        
        contexts = ["conflict", "friendship", "love", "betrayal"]
        for context in contexts:
            dialogue = llm.generate_dialogue("A", "B", context)
            assert len(dialogue) > 0
    
    def test_enhance_description(self):
        """Test description enhancement"""
        llm = MockLLMBackend(LLMConfig(provider=LLMProvider.MOCK))
        enhanced = llm.enhance_description("A dark forest")
        
        assert enhanced is not None
        assert isinstance(enhanced, str)
    
    def test_suggest_plot_twist(self):
        """Test plot twist suggestion"""
        llm = MockLLMBackend(LLMConfig(provider=LLMProvider.MOCK))
        twists = llm.suggest_plot_twist("fantasy", "Hero fights dragon", complexity=2)
        
        assert twists is not None
        assert isinstance(twists, str)


class TestToolkitWithLLM:
    """Test StoryToolkit integration with LLM"""
    
    def test_toolkit_creation_with_llm(self, mock_llm_backend):
        """Test creating StoryToolkit with LLM backend"""
        toolkit = StoryToolkit(llm_backend=mock_llm_backend)
        
        assert toolkit._llm_backend is not None
        assert toolkit.dialogue_gen.use_llm is True
    
    def test_get_llm_status(self, mock_llm_backend):
        """Test get_llm_status method"""
        toolkit = StoryToolkit(llm_backend=mock_llm_backend)
        status = toolkit.get_llm_status()
        
        assert status["available"] is True
        assert status["provider"] == "mock"
    
    def test_generate_advanced_dialogue(self, mock_llm_backend):
        """Test generate_advanced_dialogue method"""
        toolkit = StoryToolkit(llm_backend=mock_llm_backend)
        dialogue = toolkit.generate_advanced_dialogue(
            speaker="Hero",
            listener="Villain",
            context="conflict",
            style="dramatic",
            num_lines=4
        )
        
        assert isinstance(dialogue, list)
        assert len(dialogue) > 0
    
    def test_generate_advanced_dialogue_without_llm(self):
        """Test that advanced dialogue raises error without LLM"""
        toolkit = StoryToolkit()  # No LLM
        
        with pytest.raises(RuntimeError) as exc_info:
            toolkit.generate_advanced_dialogue("A", "B", "conflict")
        
        assert "LLM backend" in str(exc_info.value)
    
    def test_full_story_with_advanced_dialogue(self, mock_llm_backend):
        """Test generating full story with advanced dialogue"""
        toolkit = StoryToolkit(llm_backend=mock_llm_backend)
        
        story = toolkit.generate_full_story(
            genre="fantasy",
            theme="courage",
            num_characters=2,
            use_advanced_dialogue=True
        )
        
        assert story is not None
        assert "metadata" in story
        assert story["metadata"]["has_llm"] is True