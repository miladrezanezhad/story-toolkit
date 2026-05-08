"""
SQLite backend for long-term memory storage.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sqlite3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import uuid

from .base import BaseMemory, MemoryConfig, MemoryProvider
from .models import (
    StoryModel, EventModel, CharacterModel, LocationModel,
    ConsistencyIssue, EventType, ArcStage
)


class SQLiteMemory(BaseMemory):
    """SQLite backend for persistent story storage"""
    
    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()
    
    def _init_db(self):
        """Initialize database and create tables"""
        # Create directory if needed
        db_dir = Path(self.config.db_path).parent
        if db_dir and not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
        
        # Connect to database
        self.conn = sqlite3.connect(self.config.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create all tables
        self._create_tables()
    
    def _create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()
        
        # Stories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stories (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                genre TEXT NOT NULL,
                theme TEXT NOT NULL,
                description TEXT,
                author TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                data TEXT
            )
        """)
        
        # Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id TEXT NOT NULL,
                chapter INTEGER NOT NULL,
                sequence INTEGER DEFAULT 0,
                description TEXT NOT NULL,
                event_type TEXT NOT NULL,
                importance INTEGER DEFAULT 3,
                characters TEXT,
                location TEXT,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)
        
        # Characters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                age INTEGER DEFAULT 0,
                traits TEXT,
                goals TEXT,
                skills TEXT,
                weaknesses TEXT,
                fears TEXT,
                relationships TEXT,
                arc_stage TEXT NOT NULL,
                background TEXT,
                notes TEXT,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)
        
        # Locations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                name TEXT NOT NULL,
                location_type TEXT NOT NULL,
                description TEXT,
                connected_to TEXT,
                notes TEXT,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)
        
        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_story_id ON events(story_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_chapter ON events(story_id, chapter)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_characters_story_id ON characters(story_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_locations_story_id ON locations(story_id)")
        
        self.conn.commit()
    
    def connect(self):
        """Establish connection (already done in init)"""
        if not self.conn:
            self._init_db()
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    # ==================== Story Methods ====================
    
    def save_story(self, story: StoryModel) -> str:
        """Save story to database"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO stories 
            (id, name, genre, theme, description, author, created_at, updated_at, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            story.id,
            story.name,
            story.genre,
            story.theme,
            story.description,
            story.author,
            story.created_at.isoformat(),
            story.updated_at.isoformat(),
            json.dumps(story.data, ensure_ascii=False) if story.data else None
        ))
        
        self.conn.commit()
        return story.id
    
    def load_story(self, story_id: str) -> Optional[StoryModel]:
        """Load story from database"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT * FROM stories WHERE id = ?", (story_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return StoryModel(
            id=row['id'],
            name=row['name'],
            genre=row['genre'],
            theme=row['theme'],
            description=row['description'] or "",
            author=row['author'] or "",
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
            data=json.loads(row['data']) if row['data'] else {}
        )
    
    def list_stories(self) -> List[StoryModel]:
        """List all stories"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM stories ORDER BY updated_at DESC")
        
        stories = []
        for row in cursor.fetchall():
            stories.append(StoryModel(
                id=row['id'],
                name=row['name'],
                genre=row['genre'],
                theme=row['theme'],
                description=row['description'] or "",
                author=row['author'] or "",
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at']),
                data=json.loads(row['data']) if row['data'] else {}
            ))
        
        return stories
    
    def delete_story(self, story_id: str) -> bool:
        """Delete story from database"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM stories WHERE id = ?", (story_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_story(self, story: StoryModel) -> bool:
        """Update existing story"""
        story.updated_at = datetime.now()
        self.save_story(story)
        return True
    
    # ==================== Event Methods ====================
    
    def add_event(self, event: EventModel) -> int:
        """Add event to timeline"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO events 
            (story_id, chapter, sequence, description, event_type, importance, characters, location, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.story_id,
            event.chapter,
            event.sequence,
            event.description,
            event.event_type.value if isinstance(event.event_type, EventType) else event.event_type,
            event.importance,
            json.dumps(event.characters) if event.characters else None,
            event.location,
            event.timestamp.isoformat()
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_events(self, story_id: str, chapter: Optional[int] = None) -> List[EventModel]:
        """Get events for a story"""
        cursor = self.conn.cursor()
        
        if chapter:
            cursor.execute("""
                SELECT * FROM events 
                WHERE story_id = ? AND chapter = ? 
                ORDER BY sequence, timestamp
            """, (story_id, chapter))
        else:
            cursor.execute("""
                SELECT * FROM events 
                WHERE story_id = ? 
                ORDER BY chapter, sequence, timestamp
            """, (story_id,))
        
        events = []
        for row in cursor.fetchall():
            events.append(EventModel(
                id=row['id'],
                story_id=row['story_id'],
                chapter=row['chapter'],
                sequence=row['sequence'] or 0,
                description=row['description'],
                event_type=EventType(row['event_type']),
                importance=row['importance'],
                characters=json.loads(row['characters']) if row['characters'] else [],
                location=row['location'] or "",
                timestamp=datetime.fromisoformat(row['timestamp'])
            ))
        
        return events
    
    def get_timeline(self, story_id: str) -> List[EventModel]:
        """Get chronological timeline"""
        return self.get_events(story_id)
    
    def delete_event(self, event_id: int) -> bool:
        """Delete an event"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # ==================== Character Methods ====================
    
    def save_character(self, character: CharacterModel) -> str:
        """Save character to database"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO characters 
            (id, story_id, name, role, age, traits, goals, skills, weaknesses, fears, relationships, arc_stage, background, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            character.id,
            character.story_id,
            character.name,
            character.role,
            character.age,
            json.dumps(character.traits),
            json.dumps(character.goals),
            json.dumps(character.skills),
            json.dumps(character.weaknesses),
            json.dumps(character.fears),
            json.dumps(character.relationships),
            character.arc_stage.value if isinstance(character.arc_stage, ArcStage) else character.arc_stage,
            character.background,
            character.notes
        ))
        
        self.conn.commit()
        return character.id
    
    def load_character(self, character_id: str) -> Optional[CharacterModel]:
        """Load a single character"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return CharacterModel(
            id=row['id'],
            story_id=row['story_id'],
            name=row['name'],
            role=row['role'],
            age=row['age'] or 0,
            traits=json.loads(row['traits']) if row['traits'] else [],
            goals=json.loads(row['goals']) if row['goals'] else [],
            skills=json.loads(row['skills']) if row['skills'] else [],
            weaknesses=json.loads(row['weaknesses']) if row['weaknesses'] else [],
            fears=json.loads(row['fears']) if row['fears'] else [],
            relationships=json.loads(row['relationships']) if row['relationships'] else {},
            arc_stage=ArcStage(row['arc_stage']),
            background=row['background'] or "",
            notes=row['notes'] or ""
        )
    
    def load_characters(self, story_id: str) -> List[CharacterModel]:
        """Load all characters for a story"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM characters WHERE story_id = ?", (story_id,))
        
        characters = []
        for row in cursor.fetchall():
            char = self.load_character(row['id'])
            if char:
                characters.append(char)
        
        return characters
    
    def delete_character(self, character_id: str) -> bool:
        """Delete a character"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM characters WHERE id = ?", (character_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # ==================== Location Methods ====================
    
    def save_location(self, location: LocationModel) -> str:
        """Save location to database"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO locations 
            (id, story_id, name, location_type, description, connected_to, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            location.id,
            location.story_id,
            location.name,
            location.location_type,
            location.description,
            json.dumps(location.connected_to) if location.connected_to else None,
            location.notes
        ))
        
        self.conn.commit()
        return location.id
    
    def load_locations(self, story_id: str) -> List[LocationModel]:
        """Load all locations for a story"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM locations WHERE story_id = ?", (story_id,))
        
        locations = []
        for row in cursor.fetchall():
            locations.append(LocationModel(
                id=row['id'],
                story_id=row['story_id'],
                name=row['name'],
                location_type=row['location_type'],
                description=row['description'] or "",
                connected_to=json.loads(row['connected_to']) if row['connected_to'] else [],
                notes=row['notes'] or ""
            ))
        
        return locations
    
    def delete_location(self, location_id: str) -> bool:
        """Delete a location"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # ==================== Consistency Methods ====================
    
    def check_consistency(self, story_id: str) -> List[ConsistencyIssue]:
        """Check for inconsistencies in story"""
        issues = []
        
        # Get all events
        events = self.get_events(story_id)
        
        # Check for timeline issues
        prev_time = None
        prev_chapter = 0
        for event in events:
            if prev_time and event.timestamp < prev_time:
                issues.append(ConsistencyIssue(
                    issue_type="timeline",
                    severity="high",
                    description=f"Event '{event.description[:50]}' occurs before previous event",
                    location=f"Chapter {event.chapter}"
                ))
            prev_time = event.timestamp
            
            # Check chapter order
            if event.chapter < prev_chapter:
                issues.append(ConsistencyIssue(
                    issue_type="chapter_order",
                    severity="medium",
                    description=f"Chapter {event.chapter} appears after chapter {prev_chapter}",
                    location=f"Event: {event.description[:50]}"
                ))
            prev_chapter = event.chapter
        
        # Get all characters
        characters = self.load_characters(story_id)
        
        # Check character arc consistency
        valid_stages = ["initial", "challenged", "transformation", "new_equilibrium"]
        for char in characters:
            if char.arc_stage.value not in valid_stages:
                issues.append(ConsistencyIssue(
                    issue_type="character_arc",
                    severity="medium",
                    description=f"Invalid arc stage for '{char.name}': {char.arc_stage.value}",
                    suggestion="Valid stages: initial, challenged, transformation, new_equilibrium"
                ))
        
        return issues
    
    # ==================== Search Methods ====================
    
    def search_events(self, story_id: str, query: str) -> List[EventModel]:
        """Search events by keyword"""
        events = self.get_events(story_id)
        results = []
        
        query_lower = query.lower()
        for event in events:
            if query_lower in event.description.lower():
                results.append(event)
        
        return results
    
    def search_characters(self, story_id: str, query: str) -> List[CharacterModel]:
        """Search characters by name or trait"""
        characters = self.load_characters(story_id)
        results = []
        
        query_lower = query.lower()
        for char in characters:
            if (query_lower in char.name.lower() or
                any(query_lower in trait.lower() for trait in char.traits)):
                results.append(char)
        
        return results
    
    # ==================== Stats Methods ====================
    
    def get_story_stats(self, story_id: str) -> Dict[str, Any]:
        """Get statistics about a story"""
        events = self.get_events(story_id)
        characters = self.load_characters(story_id)
        locations = self.load_locations(story_id)
        
        return {
            "total_events": len(events),
            "total_characters": len(characters),
            "total_locations": len(locations),
            "chapters": max([e.chapter for e in events]) if events else 0,
            "avg_importance": sum(e.importance for e in events) / len(events) if events else 0,
            "event_types": {}
        }
    
    # ==================== Utility Methods ====================
    
    def clear_story(self, story_id: str) -> bool:
        """Delete all data for a story"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM events WHERE story_id = ?", (story_id,))
        cursor.execute("DELETE FROM characters WHERE story_id = ?", (story_id,))
        cursor.execute("DELETE FROM locations WHERE story_id = ?", (story_id,))
        cursor.execute("DELETE FROM stories WHERE id = ?", (story_id,))
        self.conn.commit()
        return True
    
    def vacuum(self):
        """Optimize database (remove deleted data)"""
        self.conn.execute("VACUUM")
        self.conn.commit()
