"""
Story Development Toolkit
========================
A comprehensive toolkit for generating engaging and coherent stories.
Provides tools for character creation, plot generation, dialogue writing,
and story coherence checking.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from .core.story_engine import StoryEngine
from .core.character import Character
from .core.plot import Plot
from .core.world_builder import WorldBuilder
from .generators.character_generator import CharacterGenerator
from .generators.plot_generator import PlotGenerator
from .generators.dialogue_generator import DialogueGenerator
from .nlp.coherence_checker import CoherenceChecker
from .nlp.text_analyzer import TextAnalyzer
from .utils.helpers import save_story, load_story, export_to_markdown

__version__ = "1.0.0"
__author__ = "Milad Rezanezhad"
__github__ = "https://github.com/miladrezanezhad"

class StoryToolkit:
    """Main interface for accessing all toolkit features"""
    
    def __init__(self):
        self.engine = StoryEngine()
        self.character_gen = CharacterGenerator()
        self.plot_gen = PlotGenerator()
        self.dialogue_gen = DialogueGenerator()
        self.coherence_checker = CoherenceChecker()
        self.text_analyzer = TextAnalyzer()
        
    def create_story(self, genre: str, theme: str, complexity: int = 3) -> dict:
        """Create a complete story with all elements"""
        from datetime import datetime
        
        story = {
            "metadata": {
                "genre": genre,
                "theme": theme,
                "complexity": complexity,
                "created_at": datetime.now().isoformat(),
                "toolkit_version": __version__
            },
            "outline": self.engine.create_story_outline(genre, theme),
            "plot": self.plot_gen.generate_plot(genre, complexity),
            "characters": [],
            "world": {},
            "dialogue_scenes": [],
            "coherence_report": None
        }
        return story
    
    def add_character_to_story(self, story: dict, name: str, role: str) -> Character:
        """Add a new character to the story"""
        import random
        
        character = Character(
            name=name,
            age=random.randint(20, 60),
            role=role
        )
        story["characters"].append(character)
        return character
    
    def check_story_coherence(self, story_data: dict) -> dict:
        """Check story coherence and generate a report"""
        report = self.coherence_checker.generate_coherence_report(story_data)
        story_data["coherence_report"] = report
        return report
    
    def generate_full_story(self, genre: str, theme: str, num_characters: int = 3) -> dict:
        """Generate a complete story with all elements automatically"""
        from datetime import datetime
        
        # Create story framework
        story = self.create_story(genre, theme)
        story["metadata"]["created_at"] = datetime.now().isoformat()
        
        # Generate characters
        roles = ["protagonist", "antagonist", "supporting", "mentor"]
        for i in range(min(num_characters, len(roles))):
            char = self.character_gen.generate_character(roles[i])
            story["characters"].append(char)
        
        # Generate world
        world_builder = WorldBuilder()
        story["world"] = world_builder.generate_world(genre)
        
        # Generate key dialogues
        if len(story["characters"]) >= 2:
            dialogue = self.dialogue_gen.generate_dialogue(
                story["characters"][0].name,
                story["characters"][1].name,
                context="conflict"
            )
            story["dialogue_scenes"].append(dialogue)
        
        # Check coherence
        story["coherence_report"] = self.check_story_coherence(story)
        
        return story
    
    def export_story(self, story: dict, format: str = "json", filename: str = None) -> str:
        """Export story to different formats (json, markdown, txt)"""
        if not filename:
            from datetime import datetime
            filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format == "json":
            return save_story(story, f"{filename}.json")
        elif format == "markdown":
            return export_to_markdown(story, f"{filename}.md")
        elif format == "txt":
            return save_story(story, f"{filename}.txt")
        else:
            raise ValueError(f"Unsupported format: {format}")

# Easy access exports
__all__ = [
    'StoryToolkit',
    'StoryEngine',
    'Character',
    'Plot',
    'WorldBuilder',
    'CharacterGenerator',
    'PlotGenerator',
    'DialogueGenerator',
    'CoherenceChecker',
    'TextAnalyzer',
    'save_story',
    'load_story',
    'export_to_markdown'
]
