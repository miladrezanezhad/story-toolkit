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
from .generators.story_generator import StoryGenerator
from .nlp.coherence_checker import CoherenceChecker
from .nlp.text_analyzer import TextAnalyzer
from .utils.helpers import save_story, load_story, export_to_markdown

# LLM module
from .llm import LLMFactory, LLMProvider, BaseLLMBackend, MockLLMBackend

# Memory module
from .memory import MemoryManager, MemoryConfig

# Templates module
from .templates import TemplateManager

__version__ = "2.3.0-dev"
__author__ = "Milad Rezanezhad"
__github__ = "https://github.com/miladrezanezhad/story-toolkit"


class StoryToolkit:
    """Main interface for accessing all toolkit features with optional LLM and memory support"""
    
    def __init__(self, llm_backend: BaseLLMBackend = None, memory_backend: str = None, db_path: str = "stories.db"):
        """
        Initialize the Story Toolkit with optional LLM and memory support.
        
        Args:
            llm_backend: Optional LLM backend for advanced generation
            memory_backend: Optional memory backend ('sqlite' or None)
            db_path: Path to database file for SQLite memory
        """
        self.engine = StoryEngine()
        self.character_gen = CharacterGenerator()
        self.plot_gen = PlotGenerator()
        self.dialogue_gen = DialogueGenerator(llm_backend=llm_backend)
        self.story_gen = StoryGenerator(llm_backend=llm_backend)
        self.coherence_checker = CoherenceChecker()
        self.text_analyzer = TextAnalyzer()
        self._llm_backend = llm_backend
        
        # Initialize memory manager
        self._memory = None
        self._current_story_id = None
        
        if memory_backend == "sqlite":
            self._memory = MemoryManager(db_path=db_path)
            print(f"📁 Memory enabled: {db_path}")
    
    def generate_novel(self, genre: str, theme: str,
                       num_chapters: int = 5,
                       words_per_chapter: int = 500,
                       protagonist_name: str = None,
                       antagonist_name: str = None,
                       use_llm: bool = True) -> dict:
        """
        Generate a complete novel automatically.
        
        Args:
            genre: fantasy, sci-fi, mystery, romance, adventure
            theme: courage, love, redemption, survival
            num_chapters: Number of chapters (default: 5)
            words_per_chapter: Words per chapter (default: 500)
            protagonist_name: Hero's name (auto-generated)
            antagonist_name: Villain's name (auto-generated)
            use_llm: Use LLM for generation (requires llm_backend)
        
        Returns:
            Complete novel as dictionary
        
        Example:
            >>> toolkit = StoryToolkit()
            >>> novel = toolkit.generate_novel("fantasy", "courage", num_chapters=3)
            >>> print(novel['chapters'][0]['content'])
        """
        return self.story_gen.generate_novel(
            genre=genre,
            theme=theme,
            num_chapters=num_chapters,
            words_per_chapter=words_per_chapter,
            protagonist_name=protagonist_name,
            antagonist_name=antagonist_name,
            use_llm=use_llm
        )
    
    def create_story(self, genre: str, theme: str, complexity: int = 3, 
                     name: str = None, save_to_memory: bool = False) -> dict:
        """Create a complete story with all elements"""
        from datetime import datetime
        
        story = {
            "metadata": {
                "genre": genre,
                "theme": theme,
                "complexity": complexity,
                "created_at": datetime.now().isoformat(),
                "toolkit_version": __version__,
                "has_llm": self._llm_backend is not None
            },
            "outline": self.engine.create_story_outline(genre, theme),
            "plot": self.plot_gen.generate_plot(genre, complexity),
            "characters": [],
            "world": {},
            "dialogue_scenes": [],
            "coherence_report": None
        }
        
        # Save to memory if requested
        if save_to_memory and self._memory:
            story_name = name or f"{genre}_{theme}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self._current_story_id = self._memory.create_story(
                name=story_name,
                genre=genre,
                theme=theme,
                description=f"A {genre} story about {theme}"
            )
            story["metadata"]["memory_id"] = self._current_story_id
            print(f"💾 Story saved to memory: {self._current_story_id}")
        
        return story
    
    def add_character_to_story(self, story: dict, name: str, role: str, save_to_memory: bool = True) -> Character:
        """Add a new character to the story"""
        import random
        
        character = Character(
            name=name,
            age=random.randint(20, 60),
            role=role
        )
        story["characters"].append(character)
        
        # Save to memory only if requested AND character doesn't already exist
        if save_to_memory and self._memory and self._current_story_id:
            existing_chars = self._memory.get_characters(self._current_story_id)
            existing_names = [c.name for c in existing_chars]
            
            if name not in existing_names:
                self._memory.add_character(
                    story_id=self._current_story_id,
                    name=name,
                    role=role,
                    traits=[]
                )
            else:
                print(f"   ⚠️ Character '{name}' already exists in database, skipping duplicate")
        
        return character
    
    def add_event(self, chapter: int, description: str, event_type: str = "general", importance: int = 5):
        """Add an event to the current story timeline"""
        if not self._memory or not self._current_story_id:
            raise RuntimeError("No story is currently active in memory. Create a story with save_to_memory=True")
        
        return self._memory.add_event(
            story_id=self._current_story_id,
            chapter=chapter,
            description=description,
            event_type=event_type,
            importance=importance
        )
    
    def get_timeline(self) -> list:
        """Get timeline of current story"""
        if not self._memory or not self._current_story_id:
            raise RuntimeError("No story is currently active in memory")
        
        return self._memory.get_timeline(self._current_story_id)
    
    def load_story_from_memory(self, story_id: str) -> dict:
        """Load a story from memory into the toolkit"""
        if not self._memory:
            raise RuntimeError("Memory backend not enabled")
        
        story_data = self._memory.get_story(story_id)
        if not story_data:
            raise ValueError(f"Story {story_id} not found")
        
        self._current_story_id = story_id
        
        # Reconstruct story dict from memory
        story = {
            "metadata": {
                "genre": story_data.genre,
                "theme": story_data.theme,
                "memory_id": story_id,
                "name": story_data.name,
                "description": story_data.description,
                "created_at": story_data.created_at.isoformat(),
                "toolkit_version": __version__
            },
            "outline": {},
            "plot": {},
            "characters": [],
            "world": {},
            "dialogue_scenes": [],
            "coherence_report": None
        }
        
        # Load characters from memory
        characters = self._memory.get_characters(story_id)
        for char_data in characters:
            existing_names = [c.name for c in story["characters"]]
            if char_data.name not in existing_names:
                char = self.add_character_to_story(story, char_data.name, char_data.role, save_to_memory=False)
                char.traits = char_data.traits
                char.goals = char_data.goals
        
        print(f"📖 Story loaded: {story_data.name}")
        return story
    
    def list_stored_stories(self) -> list:
        """List all stories in memory"""
        if not self._memory:
            raise RuntimeError("Memory backend not enabled")
        
        return self._memory.list_stories()
    
    def use_template(self, template_name: str, genre: str = None, theme: str = None) -> dict:
        """Create a story using a pre-built template"""
        manager = TemplateManager()
        return manager.create_story_from_template(template_name, genre, theme)
    
    def list_templates(self) -> list:
        """List all available story templates"""
        manager = TemplateManager()
        return manager.list_templates()
    
    def get_template_info(self, template_name: str) -> dict:
        """Get detailed information about a template"""
        manager = TemplateManager()
        info = manager.get_template_info(template_name)
        if not info:
            raise ValueError(f"Template '{template_name}' not found")
        return info
    
    def get_template_names(self) -> list:
        """Get all available template names"""
        manager = TemplateManager()
        return manager.get_template_names()
    
    def check_story_coherence(self, story_data: dict) -> dict:
        """Check story coherence and generate a report"""
        report = self.coherence_checker.generate_coherence_report(story_data)
        story_data["coherence_report"] = report
        return report
    
    def generate_full_story(self, genre: str, theme: str, num_characters: int = 3, 
                           use_advanced_dialogue: bool = False,
                           save_to_memory: bool = False) -> dict:
        """Generate a complete story with all elements automatically"""
        from datetime import datetime
        
        # Create story framework
        story = self.create_story(genre, theme, save_to_memory=save_to_memory)
        story["metadata"]["created_at"] = datetime.now().isoformat()
        
        # Generate characters
        roles = ["protagonist", "antagonist", "supporting", "mentor"]
        for i in range(min(num_characters, len(roles))):
            char = self.character_gen.generate_character(roles[i])
            story["characters"].append(char)
            
            if save_to_memory and self._memory and self._current_story_id:
                self._memory.add_character(
                    story_id=self._current_story_id,
                    name=char.name,
                    role=char.role,
                    traits=char.personality_traits
                )
        
        # Generate world
        world_builder = WorldBuilder()
        story["world"] = world_builder.generate_world(genre)
        
        # Generate key dialogues
        if len(story["characters"]) >= 2:
            dialogue = self.dialogue_gen.generate_dialogue(
                story["characters"][0].name,
                story["characters"][1].name,
                context="conflict",
                use_advanced=use_advanced_dialogue,
                style="dramatic" if use_advanced_dialogue else None,
                num_lines=8 if use_advanced_dialogue else 5
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
    
    def get_llm_status(self) -> dict:
        """Get status of LLM integration"""
        return {
            "available": self._llm_backend is not None,
            "provider": self._llm_backend.config.provider.value if self._llm_backend else None,
            "model": self._llm_backend.config.model if self._llm_backend else None
        }
    
    def generate_advanced_dialogue(self, speaker: str, listener: str, context: str,
                                   style: str = "natural", num_lines: int = 5) -> list:
        """Generate advanced dialogue using LLM (if available)"""
        if not self._llm_backend:
            raise RuntimeError(
                "Advanced dialogue generation requires an LLM backend. "
                "Initialize StoryToolkit with llm_backend parameter."
            )
        
        return self._llm_backend.generate_dialogue(
            speaker=speaker,
            listener=listener,
            context=context,
            style=style,
            num_lines=num_lines
        )
    
    def close_memory(self):
        """Close memory database connection"""
        if self._memory:
            self._memory.close()
            print("🔒 Memory database closed")
    
    def get_current_story_id(self) -> str:
        """Get current active story ID"""
        return self._current_story_id


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
    'StoryGenerator',
    'CoherenceChecker',
    'TextAnalyzer',
    'save_story',
    'load_story',
    'export_to_markdown',
    'LLMFactory',
    'LLMProvider',
    'BaseLLMBackend',
    'MockLLMBackend',
    'MemoryManager',
    'MemoryConfig',
    'TemplateManager'
]
