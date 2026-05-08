"""
Template manager for story-toolkit.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import Dict, List, Optional, Any
from .base import BaseTemplate
from .hero_journey import HeroJourneyTemplate
from .three_act import ThreeActTemplate
from .mystery_clues import MysteryCluesTemplate
from .romance_beat import RomanceBeatTemplate
from .horror_cycle import HorrorCycleTemplate


class TemplateManager:
    """Manager for all story templates"""
    
    def __init__(self):
        self._templates: Dict[str, BaseTemplate] = {}
        self._register_templates()
    
    def _register_templates(self):
        """Register all available templates"""
        templates = [
            HeroJourneyTemplate(),
            ThreeActTemplate(),
            MysteryCluesTemplate(),
            RomanceBeatTemplate(),
            HorrorCycleTemplate()
        ]
        
        for template in templates:
            self._templates[template.name] = template
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates"""
        return [
            {
                "name": t.name,
                "genre": t.genre,
                "description": t.description,
                "stage_count": t.get_stage_count()
            }
            for t in self._templates.values()
        ]
    
    def get_template(self, name: str) -> Optional[BaseTemplate]:
        """Get template by name"""
        return self._templates.get(name)
    
    def get_template_names(self) -> List[str]:
        """Get all template names"""
        return list(self._templates.keys())
    
    def apply_template(self, name: str, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a template to existing story data"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template '{name}' not found. Available: {self.get_template_names()}")
        
        # Apply template structure to story
        stages = template.get_stages()
        
        story_data["plot"] = story_data.get("plot", {})
        story_data["plot"]["main_plot"] = [
            {
                "stage": stage.name,
                "description": stage.description,
                "chapter_range": stage.chapter_range
            }
            for stage in stages
        ]
        
        story_data["metadata"] = story_data.get("metadata", {})
        story_data["metadata"]["template"] = name
        
        return story_data
    
    def create_story_from_template(self, name: str, genre: str = None, theme: str = None) -> Dict[str, Any]:
        """Create a complete story from a template"""
        from story_toolkit import StoryToolkit
        
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template '{name}' not found")
        
        toolkit = StoryToolkit()
        
        # Use template's genre if not specified
        if genre is None:
            genre = template.genre.split(",")[0].strip()
        
        story = toolkit.create_story(genre=genre, theme=theme or "adventure")
        
        # Apply template structure
        story = self.apply_template(name, story)
        
        return story
    
    def get_template_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a template"""
        template = self.get_template(name)
        if not template:
            return None
        
        return template.to_dict()