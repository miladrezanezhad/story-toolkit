"""
Base classes for memory backends.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MemoryProvider(str, Enum):
    """Memory backend providers"""
    SQLITE = "sqlite"
    IN_MEMORY = "in_memory"


@dataclass
class MemoryConfig:
    """Configuration for memory backend"""
    provider: MemoryProvider = MemoryProvider.SQLITE
    db_path: str = "stories.db"
    auto_save: bool = True
    cache_size: int = 100


@dataclass
class StoryData:
    """Story data structure for storage"""
    id: str
    name: str
    genre: str
    theme: str
    created_at: datetime
    updated_at: datetime
    data: Dict[str, Any]


@dataclass
class EventData:
    """Event data structure for timeline"""
    id: int
    story_id: str
    chapter: int
    description: str
    event_type: str  # plot, dialogue, character_development, etc.
    importance: int  # 1-10
    timestamp: datetime


@dataclass
class CharacterData:
    """Character data structure for storage"""
    id: str
    story_id: str
    name: str
    role: str
    traits: List[str]
    goals: List[str]
    skills: List[str]
    relationships: Dict[str, Any]
    arc_stage: str


class BaseMemory(ABC):
    """Abstract base class for memory backends"""
    
    def __init__(self, config: MemoryConfig):
        self.config = config
    
    @abstractmethod
    def connect(self):
        """Establish connection to database"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close database connection"""
        pass
    
    # Story methods
    @abstractmethod
    def save_story(self, story: StoryData) -> str:
        """Save story to database"""
        pass
    
    @abstractmethod
    def load_story(self, story_id: str) -> Optional[StoryData]:
        """Load story from database"""
        pass
    
    @abstractmethod
    def list_stories(self) -> List[StoryData]:
        """List all stories"""
        pass
    
    @abstractmethod
    def delete_story(self, story_id: str) -> bool:
        """Delete story from database"""
        pass
    
    # Event methods
    @abstractmethod
    def add_event(self, event: EventData) -> int:
        """Add event to timeline"""
        pass
    
    @abstractmethod
    def get_events(self, story_id: str, chapter: Optional[int] = None) -> List[EventData]:
        """Get events for a story"""
        pass
    
    @abstractmethod
    def get_timeline(self, story_id: str) -> List[EventData]:
        """Get chronological timeline"""
        pass
    
    # Character methods
    @abstractmethod
    def save_character(self, character: CharacterData) -> str:
        """Save character to database"""
        pass
    
    @abstractmethod
    def load_characters(self, story_id: str) -> List[CharacterData]:
        """Load all characters for a story"""
        pass
    
    # Consistency methods
    @abstractmethod
    def check_consistency(self, story_id: str) -> List[Dict[str, Any]]:
        """Check for inconsistencies in story"""
        pass