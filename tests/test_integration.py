"""
Integration tests for story-toolkit

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import pytest
import json
import tempfile
import os
from story_toolkit import StoryToolkit
from story_toolkit.utils.helpers import save_story, load_story, export_to_markdown


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_story_creation_workflow(self):
        """Test complete story creation workflow"""
        toolkit = StoryToolkit()
        
        # Create story
        story = toolkit.create_story(genre="fantasy", theme="redemption")
        
        # Add characters
        hero = toolkit.add_character_to_story(story, "Kaelen", "protagonist")
        hero.add_trait("brave")
        hero.add_goal("Save the kingdom")
        
        villain = toolkit.add_character_to_story(story, "Morgath", "antagonist")
        villain.add_trait("cunning")
        
        # Generate dialogue
        dialogue = toolkit.dialogue_gen.generate_dialogue("Kaelen", "Morgath", context="conflict")
        story["dialogue_scenes"].append(dialogue)
        
        # Check coherence
        report = toolkit.check_story_coherence(story)
        
        assert report is not None
        assert "overall_score" in report
        assert len(story["characters"]) == 2
        assert len(dialogue) > 0
    
    def test_save_and_load_story(self, sample_story):
        """Test saving and loading story to/from file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Save story
            save_story(sample_story, tmp_path)
            assert os.path.exists(tmp_path)
            
            # Load story
            loaded_story = load_story(tmp_path)
            assert loaded_story is not None
            
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_export_to_markdown(self, sample_story):
        """Test exporting story to markdown"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Export to markdown
            export_to_markdown(sample_story, tmp_path)
            assert os.path.exists(tmp_path)
            
            # Check content
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 0
                
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_full_story_generation(self):
        """Test automatic full story generation"""
        toolkit = StoryToolkit()
        
        story = toolkit.generate_full_story(
            genre="sci-fi",
            theme="survival",
            num_characters=3
        )
        
        assert story is not None
        assert "metadata" in story
        assert "characters" in story
        assert "plot" in story
        assert len(story["characters"]) >= 2
    
    def test_toolkit_version(self):
        """Test toolkit version"""
        from story_toolkit import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)


class TestBackwardCompatibility:
    """Tests to ensure backward compatibility"""
    
    def test_old_interface_still_works(self):
        """Test that code written for v1.0.0 still works"""
        # This mimics how users used the library before LLM addition
        from story_toolkit import StoryToolkit
        from story_toolkit.core.character import Character
        
        toolkit = StoryToolkit()
        
        # Old way of creating story
        story = toolkit.create_story(genre="fantasy", theme="courage")
        
        # Old way of adding character
        hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
        hero.add_trait("brave")
        
        # Old way of generating dialogue (no use_advanced parameter)
        dialogue = toolkit.dialogue_gen.generate_dialogue("Kai", "Villain", context="conflict")
        
        # Old way of checking coherence
        report = toolkit.check_story_coherence(story)
        
        assert dialogue is not None
        assert report is not None
        assert hero.traits == ["brave"]
    
    def test_old_dialogue_generator_init_still_works(self):
        """Test that DialogueGenerator can be initialized without parameters"""
        from story_toolkit.generators.dialogue_generator import DialogueGenerator
        
        # Old way - no parameters
        generator = DialogueGenerator()
        
        assert generator.use_llm is False
        assert generator.llm_backend is None