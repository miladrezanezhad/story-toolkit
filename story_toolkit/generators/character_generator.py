"""
Character Generator Module
==========================
Generates random or templated characters for stories.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import random
from typing import List, Dict, Optional
from ..core.character import Character

class CharacterGenerator:
    """Generates characters with random or specified attributes"""
    
    def __init__(self):
        # Name pools for character generation
        self.first_names = [
            "Alexander", "Sophia", "Marcus", "Elena", "Kai",
            "Luna", "Atlas", "Nova", "Orion", "Aria",
            "Zane", "Iris", "Phoenix", "Sage", "Ruby"
        ]
        
        self.last_names = [
            "Blackwood", "Storm", "Raven", "Winter", "Stone",
            "Nightshade", "Frost", "Shadow", "Drake", "Moon"
        ]
        
        # Trait pools
        self.positive_traits = [
            "brave", "intelligent", "compassionate", "determined",
            "creative", "loyal", "resourceful", "charismatic",
            "wise", "resilient", "honest", "optimistic"
        ]
        
        self.neutral_traits = [
            "ambitious", "cautious", "mysterious", "proud",
            "sarcastic", "stoic", "stubborn", "curious"
        ]
        
        self.negative_traits = [
            "arrogant", "impulsive", "jealous", "manipulative",
            "paranoid", "reckless", "vengeful", "greedy"
        ]
        
        # Role-specific templates
        self.role_templates = {
            "protagonist": {
                "traits": ["brave", "determined", "compassionate"],
                "goals": ["save the world", "protect loved ones", "discover truth"],
                "arc": "hero_journey"
            },
            "antagonist": {
                "traits": ["ambitious", "intelligent", "manipulative"],
                "goals": ["gain power", "seek revenge", "impose order"],
                "arc": "villain_fall"
            },
            "mentor": {
                "traits": ["wise", "patient", "mysterious"],
                "goals": ["guide the hero", "protect knowledge", "atone for past"],
                "arc": "mentor_sacrifice"
            },
            "supporting": {
                "traits": ["loyal", "humorous", "resourceful"],
                "goals": ["help friends", "find purpose", "overcome fear"],
                "arc": "sidekick_growth"
            }
        }
        
        # Background templates
        self.backgrounds = [
            "orphaned at young age, raised by mentors",
            "from noble family seeking adventure",
            "commoner who discovered hidden talent",
            "exiled from homeland, seeking redemption",
            "scholar who uncovered forbidden knowledge",
            "warrior haunted by past failures",
            "artist who sees the world differently"
        ]
        
    def generate_character(self, role: str = "supporting", 
                          complexity: int = 3) -> Character:
        """
        Generate a random character.
        
        Args:
            role: Character role (protagonist, antagonist, etc.)
            complexity: Number of traits and attributes to generate
            
        Returns:
            Generated Character object
        """
        # Generate name
        name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
        
        # Create character
        character = Character(
            name=name,
            age=random.randint(18, 70),
            role=role
        )
        
        # Apply role-specific template
        if role in self.role_templates:
            template = self.role_templates[role]
            for trait in template["traits"][:complexity]:
                character.add_trait(trait)
            character.add_goal(random.choice(template["goals"]))
        
        # Add random traits based on complexity
        all_traits = self.positive_traits + self.neutral_traits
        for _ in range(complexity):
            trait = random.choice(all_traits)
            character.add_trait(trait)
        
        # Add weakness
        if self.negative_traits:
            weakness = random.choice(self.negative_traits)
            character.add_weakness(weakness)
        
        # Add background
        character.background = random.choice(self.backgrounds)
        
        # Add skills
        skills = ["combat", "strategy", "diplomacy", "stealth", "healing",
                 "technology", "magic", "survival", "investigation"]
        for _ in range(min(complexity, 3)):
            character.add_skill(random.choice(skills))
        
        # Add fears
        fears = ["failure", "abandonment", "darkness", "heights", 
                "betrayal", "loss of control", "the unknown"]
        character.add_fear(random.choice(fears))
        
        return character
    
    def generate_ensemble(self, num_characters: int = 4) -> List[Character]:
        """
        Generate a balanced ensemble of characters.
        
        Args:
            num_characters: Number of characters to generate
            
        Returns:
            List of Character objects
        """
        roles = ["protagonist", "antagonist", "mentor", "supporting"]
        characters = []
        
        for i in range(num_characters):
            role = roles[i % len(roles)]
            character = self.generate_character(role, complexity=4)
            characters.append(character)
        
        return characters
    
    def generate_with_backstory(self, role: str, 
                               backstory_theme: str = "redemption") -> Character:
        """
        Generate a character with a specific backstory theme.
        
        Args:
            role: Character role
            backstory_theme: Theme for the backstory
            
        Returns:
            Character with detailed backstory
        """
        character = self.generate_character(role, complexity=5)
        
        backstory_templates = {
            "redemption": f"{character.name} once made terrible mistakes and now seeks to make amends",
            "discovery": f"{character.name} discovered a hidden truth that changed everything",
            "legacy": f"{character.name} carries the weight of a powerful family legacy",
            "survival": f"{character.name} survived a catastrophe that shaped their worldview"
        }
        
        character.background = backstory_templates.get(
            backstory_theme, 
            backstory_templates["discovery"]
        )
        
        return character
    
    def __str__(self) -> str:
        return f"CharacterGenerator(available_names={len(self.first_names)})"
