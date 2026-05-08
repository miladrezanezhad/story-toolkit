"""
Data models for long-term memory storage.

These models define the structure of data stored in the database.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class EventType(str, Enum):
    """Types of events in story timeline"""
    PLOT = "plot"                       # Plot development
    DIALOGUE = "dialogue"               # Important dialogue
    CHARACTER_DEVELOPMENT = "character_development"  # Character growth
    CONFLICT = "conflict"               # Conflict/confrontation
    REVELATION = "revelation"           # Secret revealed
    RESOLUTION = "resolution"           # Problem solved
    TRANSITION = "transition"           # Scene/location change
    GENERAL = "general"                 # Generic event


class ArcStage(str, Enum):
    """Character arc stages"""
    INITIAL = "initial"                 # Start of journey
    CHALLENGED = "challenged"           # Facing obstacles
    TRANSFORMATION = "transformation"   # Changing/growing
    NEW_EQUILIBRIUM = "new_equilibrium" # Changed state


class RelationshipType(str, Enum):
    """Types of relationships between characters"""
    FRIEND = "friend"
    ENEMY = "enemy"
    FAMILY = "family"
    MENTOR = "mentor"
    ALLY = "ally"
    RIVAL = "rival"
    LOVE = "love"
    NEUTRAL = "neutral"


class Importance(int, Enum):
    """Importance levels for events"""
    TRIVIAL = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    CRITICAL = 5


@dataclass
class StoryModel:
    """
    Story model for database storage.
    
    Represents a complete story with all its metadata.
    """
    id: str                             # Unique identifier
    name: str                           # Story title
    genre: str                          # fantasy, mystery, romance, etc.
    theme: str                          # courage, love, redemption, etc.
    description: str = ""               # Short description
    author: str = ""                    # Author name
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)  # Full story data (JSON)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "theme": self.theme,
            "description": self.description,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "data": self.data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoryModel":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            genre=data["genre"],
            theme=data["theme"],
            description=data.get("description", ""),
            author=data.get("author", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if isinstance(data["created_at"], str) else data["created_at"],
            updated_at=datetime.fromisoformat(data["updated_at"]) if isinstance(data["updated_at"], str) else data["updated_at"],
            data=data.get("data", {})
        )
    
def __repr__(self) -> str:
    return f"Story(id={self.id}, name='{self.name}', genre='{self.genre}')"


@dataclass
class EventModel:
    """
    Event model for story timeline.
    
    Represents a single event in the story timeline.
    """
    id: Optional[int] = None            # Auto-increment ID
    story_id: str = ""                  # Linked story ID
    chapter: int = 1                    # Chapter number
    sequence: int = 0                   # Sequence within chapter
    description: str = ""               # Event description
    event_type: EventType = EventType.GENERAL
    importance: int = Importance.MODERATE
    characters: List[str] = field(default_factory=list)  # Character IDs involved
    location: str = ""                  # Where it happened
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            "id": self.id,
            "story_id": self.story_id,
            "chapter": self.chapter,
            "sequence": self.sequence,
            "description": self.description,
            "event_type": self.event_type.value if isinstance(self.event_type, EventType) else self.event_type,
            "importance": self.importance,
            "characters": json.dumps(self.characters),
            "location": self.location,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventModel":
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            story_id=data["story_id"],
            chapter=data["chapter"],
            sequence=data.get("sequence", 0),
            description=data["description"],
            event_type=data["event_type"] if isinstance(data["event_type"], EventType) else EventType(data["event_type"]),
            importance=data.get("importance", Importance.MODERATE),
            characters=json.loads(data["characters"]) if isinstance(data.get("characters"), str) else data.get("characters", []),
            location=data.get("location", ""),
            timestamp=datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"]
        )
    
    def __repr__(self) -> str:
        return f"Event(ch={self.chapter}, type={self.event_type}, desc='{self.description[:50]}...')"


@dataclass
class CharacterModel:
    """
    Character model for database storage.
    
    Represents a character in the story.
    """
    id: str                             # Unique identifier
    story_id: str                       # Linked story ID
    name: str                           # Character name
    role: str                           # protagonist, antagonist, supporting, mentor
    age: int = 0                        # Character age
    traits: List[str] = field(default_factory=list)      # Personality traits
    goals: List[str] = field(default_factory=list)       # Character goals
    skills: List[str] = field(default_factory=list)      # Skills/abilities
    weaknesses: List[str] = field(default_factory=list)  # Weaknesses
    fears: List[str] = field(default_factory=list)       # Fears
    relationships: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # Relationships with others
    arc_stage: ArcStage = ArcStage.INITIAL
    background: str = ""                # Backstory
    notes: str = ""                     # Additional notes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            "id": self.id,
            "story_id": self.story_id,
            "name": self.name,
            "role": self.role,
            "age": self.age,
            "traits": json.dumps(self.traits),
            "goals": json.dumps(self.goals),
            "skills": json.dumps(self.skills),
            "weaknesses": json.dumps(self.weaknesses),
            "fears": json.dumps(self.fears),
            "relationships": json.dumps(self.relationships),
            "arc_stage": self.arc_stage.value if isinstance(self.arc_stage, ArcStage) else self.arc_stage,
            "background": self.background,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CharacterModel":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            story_id=data["story_id"],
            name=data["name"],
            role=data["role"],
            age=data.get("age", 0),
            traits=json.loads(data["traits"]) if isinstance(data.get("traits"), str) else data.get("traits", []),
            goals=json.loads(data["goals"]) if isinstance(data.get("goals"), str) else data.get("goals", []),
            skills=json.loads(data["skills"]) if isinstance(data.get("skills"), str) else data.get("skills", []),
            weaknesses=json.loads(data["weaknesses"]) if isinstance(data.get("weaknesses"), str) else data.get("weaknesses", []),
            fears=json.loads(data["fears"]) if isinstance(data.get("fears"), str) else data.get("fears", []),
            relationships=json.loads(data["relationships"]) if isinstance(data.get("relationships"), str) else data.get("relationships", {}),
            arc_stage=data["arc_stage"] if isinstance(data["arc_stage"], ArcStage) else ArcStage(data["arc_stage"]),
            background=data.get("background", ""),
            notes=data.get("notes", "")
        )
    
    def add_relationship(self, name: str, rel_type: RelationshipType, strength: int = 5):
        """Add a relationship to another character"""
        self.relationships[name] = {
            "type": rel_type.value if isinstance(rel_type, RelationshipType) else rel_type,
            "strength": min(max(strength, 0), 10)  # Clamp between 0-10
        }
    
    def __repr__(self) -> str:
        return f"Character(id={self.id}, name='{self.name}', role='{self.role}')"


@dataclass
class LocationModel:
    """
    Location model for world building.
    
    Represents a location in the story world.
    """
    id: str
    story_id: str
    name: str
    location_type: str                  # city, forest, mountain, dungeon, etc.
    description: str = ""
    connected_to: List[str] = field(default_factory=list)  # Connected location IDs
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            "id": self.id,
            "story_id": self.story_id,
            "name": self.name,
            "location_type": self.location_type,
            "description": self.description,
            "connected_to": json.dumps(self.connected_to),
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LocationModel":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            story_id=data["story_id"],
            name=data["name"],
            location_type=data["location_type"],
            description=data.get("description", ""),
            connected_to=json.loads(data["connected_to"]) if isinstance(data.get("connected_to"), str) else data.get("connected_to", []),
            notes=data.get("notes", "")
        )


@dataclass
class ConsistencyIssue:
    """
    Model for consistency check issues.
    
    Represents an issue found during consistency checking.
    """
    issue_type: str                     # timeline, character, plot, etc.
    severity: str                       # low, medium, high
    description: str                    # Detailed description
    location: Optional[str] = None      # Where the issue occurs (chapter, event ID, etc.)
    suggestion: Optional[str] = None    # Suggested fix
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "type": self.issue_type,
            "severity": self.severity,
            "description": self.description,
            "location": self.location,
            "suggestion": self.suggestion
        }


# Import json for serialization
import json

# Export all models
__all__ = [
    'EventType',
    'ArcStage', 
    'RelationshipType',
    'Importance',
    'StoryModel',
    'EventModel',
    'CharacterModel',
    'LocationModel',
    'ConsistencyIssue'
]
