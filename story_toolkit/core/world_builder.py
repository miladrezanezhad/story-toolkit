"""
World Builder Module
====================
World building and setting management system.
Handles locations, world rules, cultures, and environmental details.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

@dataclass
class Location:
    """A location or setting in the story world"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    type: str = "general"  # city, building, natural, realm, etc.
    climate: str = ""
    population: str = ""
    key_features: List[str] = field(default_factory=list)
    connected_locations: List[str] = field(default_factory=list)
    significance: int = 5  # 1-10 scale
    
class WorldBuilder:
    """
    World building system for story development.
    Creates and manages fictional worlds, settings, and environments.
    """
    
    def __init__(self):
        self.name: str = ""
        self.type: str = ""  # fantasy, sci-fi, modern, historical, etc.
        self.locations: List[Location] = []
        self.cultures: List[Dict] = []
        self.rules: Dict = {
            "physical": [],     # Physical laws of the world
            "magical": [],      # Magic system rules (if applicable)
            "social": [],       # Social norms and rules
            "technological": [] # Technology level and rules
        }
        self.timeline: Dict = {}
        self.factions: List[Dict] = []
        
    def create_world(self, name: str, world_type: str) -> Dict:
        """Initialize a new world"""
        self.name = name
        self.type = world_type
        return {
            "name": name,
            "type": world_type,
            "locations": [],
            "rules": self.rules,
            "created_at": datetime.now().isoformat()
        }
    
    def add_location(self, name: str, description: str, 
                    location_type: str = "general") -> Location:
        """Add a new location to the world"""
        location = Location(
            name=name,
            description=description,
            type=location_type
        )
        self.locations.append(location)
        return location
    
    def connect_locations(self, location1: str, location2: str) -> None:
        """Create a connection between two locations"""
        for loc in self.locations:
            if loc.name == location1 and location2 not in loc.connected_locations:
                loc.connected_locations.append(location2)
            elif loc.name == location2 and location1 not in loc.connected_locations:
                loc.connected_locations.append(location1)
    
    def add_rule(self, category: str, rule: str) -> None:
        """Add a rule to the world"""
        if category in self.rules:
            self.rules[category].append(rule)
    
    def add_culture(self, name: str, description: str, 
                   customs: List[str] = None) -> Dict:
        """Add a culture or society to the world"""
        culture = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "description": description,
            "customs": customs or [],
            "values": [],
            "traditions": []
        }
        self.cultures.append(culture)
        return culture
    
    def add_faction(self, name: str, description: str, 
                   goals: List[str] = None) -> Dict:
        """Add a faction or group to the world"""
        faction = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "description": description,
            "goals": goals or [],
            "members": [],
            "alignment": "neutral"
        }
        self.factions.append(faction)
        return faction
    
    def generate_world(self, genre: str) -> Dict:
        """Generate a world based on genre"""
        world_templates = {
            "fantasy": self._generate_fantasy_world(),
            "sci_fi": self._generate_scifi_world(),
            "mystery": self._generate_mystery_world(),
            "adventure": self._generate_adventure_world()
        }
        return world_templates.get(genre, self._generate_default_world())
    
    def _generate_fantasy_world(self) -> Dict:
        """Generate a fantasy world template"""
        return {
            "type": "fantasy",
            "era": "medieval",
            "magic_system": "present",
            "key_locations": [
                "ancient_kingdom",
                "enchanted_forest",
                "hidden_valley",
                "dark_fortress"
            ],
            "races": ["humans", "elves", "dwarves"],
            "threats": ["dark_lord", "ancient_curse", "invading_force"]
        }
    
    def _generate_scifi_world(self) -> Dict:
        """Generate a sci-fi world template"""
        return {
            "type": "science_fiction",
            "era": "future",
            "technology_level": "advanced",
            "key_locations": [
                "space_station",
                "alien_planet",
                "earth_city",
                "research_facility"
            ],
            "technologies": ["ai", "space_travel", "robotics"],
            "threats": ["ai_uprising", "alien_invasion", "environmental_collapse"]
        }
    
    def _generate_mystery_world(self) -> Dict:
        """Generate a mystery world template"""
        return {
            "type": "mystery",
            "era": "modern",
            "atmosphere": "noir",
            "key_locations": [
                "crime_scene",
                "detective_office",
                "suspect_location",
                "hidden_room"
            ],
            "elements": ["clues", "red_herrings", "witnesses"]
        }
    
    def _generate_adventure_world(self) -> Dict:
        """Generate an adventure world template"""
        return {
            "type": "adventure",
            "era": "exploration_age",
            "key_locations": [
                "starting_point",
                "dangerous_path",
                "hidden_temple",
                "final_destination"
            ],
            "obstacles": ["natural_disasters", "hostile_natives", "traps"],
            "rewards": ["treasure", "knowledge", "artifact"]
        }
    
    def _generate_default_world(self) -> Dict:
        """Generate a default world template"""
        return {
            "type": "general",
            "era": "modern",
            "key_locations": ["city", "countryside", "coastal_area"],
            "elements": []
        }
    
    def get_world_summary(self) -> Dict:
        """Get a summary of the world"""
        return {
            "name": self.name,
            "type": self.type,
            "total_locations": len(self.locations),
            "total_cultures": len(self.cultures),
            "total_factions": len(self.factions),
            "rules_count": sum(len(v) for v in self.rules.values())
        }
    
    def validate_world(self) -> List[str]:
        """Validate world building completeness"""
        issues = []
        
        if not self.name:
            issues.append("World name is missing")
        if not self.locations:
            issues.append("No locations defined")
        if not self.cultures and self.type in ["fantasy", "sci_fi"]:
            issues.append("Consider adding cultures for this world type")
        
        return issues
    
    def __str__(self) -> str:
        return f"WorldBuilder(name='{self.name}', type='{self.type}', locations={len(self.locations)})"
    
    def __repr__(self) -> str:
        return self.__str__()
