# story_toolkit/memory/memory_manager.py

from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from .base import MemoryConfig, MemoryProvider
from .sqlite_backend import SQLiteMemory
from .models import StoryModel, EventModel, CharacterModel, ArcStage, EventType


class MemoryManager:
    """High-level manager for story memory operations"""
    
    def __init__(self, db_path: str = "stories.db"):
        # Create config with db_path
        config = MemoryConfig(db_path=db_path)
        self.memory = SQLiteMemory(config)
    
    def create_story(self, name: str, genre: str, theme: str, 
                     description: str = "", author: str = "") -> str:
        """Create a new story"""
        story = StoryModel(
            id=str(uuid.uuid4())[:8],
            name=name,
            genre=genre,
            theme=theme,
            description=description,
            author=author
        )
        self.memory.save_story(story)
        return story.id
    
    def get_story(self, story_id: str) -> Optional[StoryModel]:
        """Get story by ID"""
        return self.memory.load_story(story_id)
    
    def list_stories(self) -> List[StoryModel]:
        """List all stories"""
        return self.memory.list_stories()
    
    def delete_story(self, story_id: str) -> bool:
        """Delete story"""
        return self.memory.delete_story(story_id)
    
    def add_event(self, story_id: str, chapter: int, description: str,
                  event_type: str = "general", importance: int = 5) -> int:
        """Add an event to story timeline"""
        event = EventModel(
            story_id=story_id,
            chapter=chapter,
            description=description,
            event_type=EventType(event_type),
            importance=importance
        )
        return self.memory.add_event(event)
    
    def get_timeline(self, story_id: str) -> List[EventModel]:
        """Get story timeline"""
        return self.memory.get_events(story_id)
    
    def add_character(self, story_id: str, name: str, role: str,
                      traits: List[str] = None) -> str:
        """Add a character to story"""
        char_id = str(uuid.uuid4())[:8]
        character = CharacterModel(
            id=char_id,
            story_id=story_id,
            name=name,
            role=role,
            traits=traits or [],
            arc_stage=ArcStage.INITIAL
        )
        self.memory.save_character(character)
        return char_id
    
    def get_characters(self, story_id: str) -> List[CharacterModel]:
        """Get all characters in story"""
        return self.memory.load_characters(story_id)
    
    def search(self, story_id: str, query: str) -> List[EventModel]:
        """Search events by keyword"""
        return self.memory.search_events(story_id, query)
    
    def check_consistency(self, story_id: str) -> List[Dict]:
        """Check story consistency"""
        issues = self.memory.check_consistency(story_id)
        return [issue.to_dict() for issue in issues]
    
    def get_stats(self, story_id: str) -> Dict[str, Any]:
        """Get story statistics"""
        return self.memory.get_story_stats(story_id)
    
    def close(self):
        """Close database connection"""
        self.memory.disconnect()