"""
Dialogue Generator Module
=========================
Generates natural-sounding dialogues between characters.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import random
from typing import List, Dict, Optional

class DialogueGenerator:
    """Generates dialogues for various story contexts"""
    
    def __init__(self):
        # Dialogue templates for different contexts
        self.dialogue_patterns = {
            "conflict": [
                [
                    "{char1}: I can't believe you would do this!",
                    "{char2}: You left me no choice.",
                    "{char1}: There's always a choice. You just chose wrong."
                ],
                [
                    "{char1}: We're done. After everything we've been through.",
                    "{char2}: You're making a mistake.",
                    "{char1}: The only mistake was trusting you."
                ],
                [
                    "{char1}: You've been lying to me this whole time.",
                    "{char2}: I was trying to protect you.",
                    "{char1}: Protect me? Or protect yourself?"
                ]
            ],
            "revelation": [
                [
                    "{char1}: There's something I need to tell you...",
                    "{char2}: What is it? You're scaring me.",
                    "{char1}: Everything you know about your past... is a lie."
                ],
                [
                    "{char1}: I know who the real killer is.",
                    "{char2}: Who? Tell me!",
                    "{char1}: It's someone you trust completely."
                ]
            ],
            "emotional": [
                [
                    "{char1}: I never meant to hurt you.",
                    "{char2}: But you did. And now everything's changed.",
                    "{char1}: Can you ever forgive me?"
                ],
                [
                    "{char1}: I'm scared. For the first time in my life, I'm truly scared.",
                    "{char2}: We'll face this together. I promise.",
                    "{char1}: What if together isn't enough?"
                ]
            ],
            "romantic": [
                [
                    "{char1}: I've been wanting to say this for so long...",
                    "{char2}: Say what?",
                    "{char1}: I love you. I've always loved you."
                ],
                [
                    "{char1}: Do you ever wonder if we're meant to be?",
                    "{char2}: Every single day.",
                    "{char1}: And what do you think?",
                    "{char2}: I think the universe has been pushing us together."
                ]
            ],
            "mysterious": [
                [
                    "{char1}: Something's not right about this place.",
                    "{char2}: I feel it too. Like we're being watched.",
                    "{char1}: We need to leave. Now."
                ]
            ]
        }
        
        # Scene setting suggestions
        self.scene_settings = {
            "confession": "a quiet coffee shop at sunset",
            "confrontation": "an abandoned warehouse in the rain",
            "romantic": "a moonlit garden in spring",
            "mystery": "a dimly lit office late at night",
            "reunion": "a crowded train station",
            "betrayal": "a rooftop overlooking the city"
        }
        
    def generate_dialogue(self, character1: str, character2: str,
                         context: str = "conversation",
                         mood: str = "neutral",
                         num_lines: int = 3) -> List[str]:
        """
        Generate dialogue between two characters.
        
        Args:
            character1: Name of first character
            character2: Name of second character
            context: Dialogue context (conflict, revelation, etc.)
            mood: Emotional mood of the dialogue
            num_lines: Number of dialogue lines to generate
            
        Returns:
            List of dialogue lines
        """
        if context in self.dialogue_patterns:
            template = random.choice(self.dialogue_patterns[context])
            dialogue = []
            
            for line in template[:num_lines]:
                formatted_line = line.format(
                    char1=character1,
                    char2=character2
                )
                dialogue.append(formatted_line)
            
            return dialogue
        
        # Default dialogue if context not found
        return [
            f"{character1}: Hello {character2}.",
            f"{character2}: {character1}. I've been expecting you.",
            f"{character1}: Then you know why I'm here."
        ]
    
    def create_conversation_scene(self, characters: List[Dict],
                                 scene_purpose: str) -> Dict:
        """
        Create a complete conversation scene.
        
        Args:
            characters: List of character dictionaries
            scene_purpose: Purpose of the scene
            
        Returns:
            Dictionary containing the complete scene
        """
        scene = {
            "purpose": scene_purpose,
            "setting": self._suggest_setting(scene_purpose),
            "time_of_day": random.choice(["morning", "afternoon", "evening", "night"]),
            "atmosphere": self._get_atmosphere(scene_purpose),
            "dialogue": [],
            "character_emotions": {},
            "subtext": []
        }
        
        # Determine character emotions
        for char in characters:
            scene["character_emotions"][char.get("name", "Unknown")] = \
                self._determine_emotion(char, scene_purpose)
        
        # Generate opening line
        if len(characters) >= 2:
            scene["dialogue"] = self.generate_dialogue(
                characters[0].get("name", "Character A"),
                characters[1].get("name", "Character B"),
                context=scene_purpose
            )
        
        return scene
    
    def _suggest_setting(self, purpose: str) -> str:
        """Suggest a setting based on scene purpose"""
        return self.scene_settings.get(purpose, "a generic location")
    
    def _get_atmosphere(self, purpose: str) -> str:
        """Determine atmosphere based on scene purpose"""
        atmosphere_map = {
            "confession": "intimate and tense",
            "confrontation": "charged and volatile",
            "romantic": "warm and tender",
            "mystery": "suspenseful and eerie",
            "reunion": "emotional and nostalgic",
            "betrayal": "shocking and painful"
        }
        return atmosphere_map.get(purpose, "neutral")
    
    def _determine_emotion(self, character: Dict, purpose: str) -> str:
        """Determine character emotion for the scene"""
        primary_emotions = {
            "confession": ["guilty", "anxious", "relieved"],
            "confrontation": ["angry", "determined", "hurt"],
            "romantic": ["hopeful", "vulnerable", "passionate"],
            "mystery": ["suspicious", "curious", "fearful"],
            "reunion": ["joyful", "overwhelmed", "nostalgic"],
            "betrayal": ["shocked", "devastated", "furious"]
        }
        
        emotions = primary_emotions.get(purpose, ["neutral"])
        return random.choice(emotions)
    
    def generate_monologue(self, character: str, topic: str, 
                          mood: str = "reflective") -> List[str]:
        """
        Generate a character monologue.
        
        Args:
            character: Character name
            topic: Monologue topic
            mood: Emotional mood
            
        Returns:
            List of monologue lines
        """
        monologues = {
            "reflective": [
                f"{character}: You know, I've been thinking about {topic}...",
                f"{character}: It's strange how things turn out sometimes.",
                f"{character}: I never expected to find myself here, but now that I am...",
                f"{character}: Everything makes sense. And nothing makes sense. All at once."
            ],
            "determined": [
                f"{character}: I've come too far to give up now.",
                f"{character}: {topic} is all that matters. Everything else is just noise.",
                f"{character}: They can try to stop me, but they don't understand.",
                f"{character}: I will succeed. I have to."
            ]
        }
        
        return monologues.get(mood, monologues["reflective"])
    
    def __str__(self) -> str:
        return f"DialogueGenerator(contexts={len(self.dialogue_patterns)})"
