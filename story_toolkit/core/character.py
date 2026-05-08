"""
Character Module
================
Character creation and management system.
Handles character attributes, relationships, and development arcs.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

@dataclass
class Character:
    """
    Character class for story development.
    Manages character attributes, traits, goals, and relationships.
    """
    name: str
    age: int = 0
    role: str = "supporting"  # protagonist, antagonist, supporting, mentor
    personality_traits: List[str] = field(default_factory=list)
    background: str = ""
    goals: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    relationships: Dict[str, Dict] = field(default_factory=dict)
    skills: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    arc_stage: str = "initial"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)
    
    # Physical attributes
    appearance: Dict[str, str] = field(default_factory=dict)
    
    # Psychological attributes
    fears: List[str] = field(default_factory=list)
    motivations: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    
    def add_trait(self, trait: str) -> None:
        """Add a personality trait to the character"""
        if trait not in self.personality_traits:
            self.personality_traits.append(trait)
    
    def remove_trait(self, trait: str) -> None:
        """Remove a personality trait from the character"""
        if trait in self.personality_traits:
            self.personality_traits.remove(trait)
    
    def add_goal(self, goal: str) -> None:
        """Add a goal for the character"""
        self.goals.append(goal)
    
    def add_conflict(self, conflict_type: str) -> str:
        """
        Create a conflict for the character.
        
        Args:
            conflict_type: Type of conflict (internal, external, moral)
            
        Returns:
            Generated conflict description
        """
        conflicts = {
            "internal": f"{self.name} struggles with inner doubts and fears",
            "external": f"{self.name} faces opposition from outside forces",
            "moral": f"{self.name} must make a difficult ethical choice",
            "relationship": f"{self.name} experiences tension in key relationships",
            "societal": f"{self.name} confronts societal expectations and norms"
        }
        conflict = conflicts.get(conflict_type, f"{self.name} faces a general conflict")
        self.conflicts.append(conflict)
        return conflict
    
    def add_relationship(self, character_name: str, relationship_type: str, 
                        strength: int = 5) -> None:
        """
        Add or update a relationship with another character.
        
        Args:
            character_name: Name of the related character
            relationship_type: Type of relationship (friend, enemy, family, etc.)
            strength: Relationship strength on scale of 1-10
        """
        self.relationships[character_name] = {
            "type": relationship_type,
            "strength": max(1, min(10, strength)),
            "history": [],
            "status": "neutral"
        }
    
    def update_relationship_status(self, character_name: str, status: str) -> None:
        """Update the status of a relationship"""
        if character_name in self.relationships:
            self.relationships[character_name]["status"] = status
    
    def add_skill(self, skill: str) -> None:
        """Add a skill to the character"""
        if skill not in self.skills:
            self.skills.append(skill)
    
    def add_weakness(self, weakness: str) -> None:
        """Add a weakness to the character"""
        if weakness not in self.weaknesses:
            self.weaknesses.append(weakness)
    
    def add_fear(self, fear: str) -> None:
        """Add a fear to the character"""
        if fear not in self.fears:
            self.fears.append(fear)
    
    def add_motivation(self, motivation: str) -> None:
        """Add a motivation for the character"""
        if motivation not in self.motivations:
            self.motivations.append(motivation)
    
    def get_character_arc(self) -> Dict:
        """Get the character's development arc"""
        return {
            "name": self.name,
            "role": self.role,
            "starting_state": self._describe_current_state(),
            "desired_state": f"Achieve: {', '.join(self.goals) if self.goals else 'TBD'}",
            "arc_stage": self.arc_stage,
            "key_challenges": self.conflicts,
            "growth_areas": self.weaknesses
        }
    
    def _describe_current_state(self) -> str:
        """Generate a description of the character's current state"""
        description = f"{self.name} is a {self.age}-year-old {self.role}"
        if self.personality_traits:
            description += f" who is {', '.join(self.personality_traits[:3])}"
        return description
    
    def advance_arc(self) -> None:
        """Advance the character's development arc"""
        stages = ["initial", "challenged", "transformation", "new_equilibrium"]
        current_index = stages.index(self.arc_stage) if self.arc_stage in stages else 0
        
        if current_index < len(stages) - 1:
            self.arc_stage = stages[current_index + 1]
    
    def get_strengths_weaknesses(self) -> Dict:
        """Get a summary of character strengths and weaknesses"""
        return {
            "strengths": {
                "skills": self.skills,
                "positive_traits": [t for t in self.personality_traits 
                                  if t not in ["arrogant", "greedy", "cruel"]],
                "support_system": len(self.relationships)
            },
            "weaknesses": {
                "personal": self.weaknesses,
                "fears": self.fears,
                "conflicts": len(self.conflicts)
            }
        }
    
    def to_dict(self) -> Dict:
        """Convert character to dictionary format"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "role": self.role,
            "traits": self.personality_traits,
            "background": self.background,
            "goals": self.goals,
            "conflicts": self.conflicts,
            "skills": self.skills,
            "weaknesses": self.weaknesses,
            "fears": self.fears,
            "motivations": self.motivations,
            "arc_stage": self.arc_stage,
            "relationships": self.relationships,
            "created_at": self.created_at
        }
    
    def __str__(self) -> str:
        return f"Character(name='{self.name}', role='{self.role}', traits={len(self.personality_traits)})"
    
    def __repr__(self) -> str:
        return self.__str__()
