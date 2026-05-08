"""
Story Engine Module
===================
Core story management and outline generation engine.
Handles story structure, chapter management, and narrative flow.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class StoryElement:
    """Base element for story components"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class StoryEngine:
    """
    Main story engine for creating and managing stories.
    Handles story structure, outlines, and narrative progression.
    """
    
    def __init__(self):
        self.title: str = ""
        self.genre: str = ""
        self.theme: str = ""
        self.author: str = "Milad Rezanezhad"
        self.characters: List = []
        self.plot_points: List = []
        self.settings: List = []
        self.chapters: List = []
        self.current_chapter: int = 0
        self.story_structure: Dict = {
            "exposition": {},
            "rising_action": [],
            "climax": {},
            "falling_action": [],
            "resolution": {}
        }
        self.story_arcs: Dict = {
            "main_arc": [],
            "character_arcs": {},
            "subplots": []
        }
        
    def create_story_outline(self, genre: str, theme: str) -> Dict:
        """
        Create a story outline based on genre and theme.
        
        Args:
            genre: Story genre (e.g., fantasy, sci-fi, mystery)
            theme: Central theme of the story
            
        Returns:
            Dictionary containing the story outline
        """
        self.genre = genre
        self.theme = theme
        
        outline = {
            "genre": genre,
            "theme": theme,
            "structure": self._generate_structure(),
            "arcs": self._generate_arcs(),
            "estimated_chapters": self._estimate_chapters(),
            "key_elements": self._identify_key_elements()
        }
        return outline
    
    def _generate_structure(self) -> Dict:
        """Generate the basic story structure"""
        return {
            "exposition": {
                "description": "Introduce characters, setting, and initial situation",
                "key_events": [],
                "characters_introduced": []
            },
            "rising_action": {
                "description": "Build tension through conflicts and challenges",
                "key_events": [],
                "complications": []
            },
            "climax": {
                "description": "The turning point of the story",
                "key_events": [],
                "confrontations": []
            },
            "falling_action": {
                "description": "Consequences of the climax unfold",
                "key_events": [],
                "resolutions": []
            },
            "resolution": {
                "description": "Final outcome and new equilibrium",
                "key_events": [],
                "character_states": {}
            }
        }
    
    def _generate_arcs(self) -> Dict:
        """Generate story arcs based on genre"""
        arcs = {
            "main_arc": self._get_genre_specific_arc(),
            "character_arcs": [],
            "subplot_templates": self._get_subplot_templates()
        }
        return arcs
    
    def _get_genre_specific_arc(self) -> Dict:
        """Return genre-specific story arc template"""
        arc_templates = {
            "fantasy": {
                "type": "hero_journey",
                "stages": [
                    "ordinary_world",
                    "call_to_adventure",
                    "refusal_of_call",
                    "meeting_mentor",
                    "crossing_threshold",
                    "tests_allies_enemies",
                    "approach_inmost_cave",
                    "ordeal",
                    "reward",
                    "road_back",
                    "resurrection",
                    "return_with_elixir"
                ]
            },
            "mystery": {
                "type": "investigation",
                "stages": [
                    "crime_discovered",
                    "initial_investigation",
                    "clues_gathered",
                    "red_herrings",
                    "breakthrough",
                    "confrontation",
                    "resolution"
                ]
            },
            "romance": {
                "type": "relationship_development",
                "stages": [
                    "meeting",
                    "connection",
                    "obstacles",
                    "separation",
                    "realization",
                    "reunion"
                ]
            }
        }
        return arc_templates.get(self.genre, arc_templates["fantasy"])
    
    def _get_subplot_templates(self) -> List[Dict]:
        """Return subplot templates"""
        return [
            {"type": "friendship", "description": "Development of friendship bonds"},
            {"type": "mentor_relationship", "description": "Growth under guidance"},
            {"type": "hidden_past", "description": "Discovery of hidden history"},
            {"type": "rivalry", "description": "Competitive relationship arc"}
        ]
    
    def _estimate_chapters(self) -> int:
        """Estimate number of chapters based on genre"""
        chapter_estimates = {
            "fantasy": 25,
            "mystery": 20,
            "romance": 18,
            "sci_fi": 22,
            "adventure": 20
        }
        return chapter_estimates.get(self.genre, 20)
    
    def _identify_key_elements(self) -> Dict:
        """Identify key story elements needed"""
        return {
            "protagonist_motivation": "",
            "central_conflict": "",
            "antagonist_goal": "",
            "stakes": "",
            "theme_expression": []
        }
    
    def add_chapter(self, chapter_title: str, chapter_content: Dict = None) -> Dict:
        """Add a new chapter to the story"""
        chapter = {
            "number": len(self.chapters) + 1,
            "title": chapter_title,
            "content": chapter_content or {},
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
        self.chapters.append(chapter)
        self.current_chapter = chapter["number"]
        return chapter
    
    def get_story_progress(self) -> Dict:
        """Get current story progress statistics"""
        return {
            "total_chapters": len(self.chapters),
            "current_chapter": self.current_chapter,
            "characters_count": len(self.characters),
            "plot_points_count": len(self.plot_points),
            "settings_count": len(self.settings),
            "is_complete": self.current_chapter >= len(self.chapters) if self.chapters else False
        }
    
    def set_story_metadata(self, title: str = None, author: str = None, 
                          description: str = None) -> None:
        """Set or update story metadata"""
        if title:
            self.title = title
        if author:
            self.author = author
        if description:
            self.story_structure["description"] = description
    
    def validate_structure(self) -> List[str]:
        """Validate story structure completeness"""
        issues = []
        
        if not self.title:
            issues.append("Story title is missing")
        if not self.genre:
            issues.append("Story genre is not set")
        if not self.theme:
            issues.append("Story theme is not defined")
        if len(self.characters) < 2:
            issues.append("Story needs at least 2 characters")
        if not self.plot_points:
            issues.append("No plot points defined")
        
        return issues
    
    def __str__(self) -> str:
        return f"StoryEngine(title='{self.title}', genre='{self.genre}', chapters={len(self.chapters)})"
    
    def __repr__(self) -> str:
        return self.__str__()
