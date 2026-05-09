"""
Dialogue Generator Module
=========================
Generates natural-sounding dialogues between characters.
Now supports optional LLM integration for advanced dialogue generation.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import random
from typing import List, Dict, Optional, Any


class DialogueGenerator:
    """Generates dialogues for various story contexts with optional LLM support"""
    
    def __init__(self, llm_backend: Any = None):
        """
        Initialize the Dialogue Generator.
        
        Args:
            llm_backend: Optional LLM backend for advanced dialogue generation
        """
        self.llm_backend = llm_backend
        self.use_llm = llm_backend is not None
        
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
                ]
            ],
            "revelation": [
                [
                    "{char1}: There's something I need to tell you...",
                    "{char2}: What is it? You're scaring me.",
                    "{char1}: Everything you know about your past... is a lie."
                ]
            ],
            "emotional": [
                [
                    "{char1}: I never meant to hurt you.",
                    "{char2}: But you did. And now everything's changed.",
                    "{char1}: Can you ever forgive me?"
                ]
            ],
            "romantic": [
                [
                    "{char1}: I've been wanting to say this for so long...",
                    "{char2}: Say what?",
                    "{char1}: I love you. I've always loved you."
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
                         num_lines: int = 3,
                         use_advanced: bool = False,
                         style: str = "natural",
                         **kwargs) -> List[str]:
        """
        Generate dialogue between two characters.
        
        Args:
            character1: Name of first character
            character2: Name of second character
            context: Dialogue context (conflict, revelation, etc.)
            mood: Emotional mood of the dialogue
            num_lines: Number of dialogue lines to generate
            use_advanced: Use LLM for advanced dialogue if available
            style: Dialogue style for advanced generation
            **kwargs: Additional parameters
            
        Returns:
            List of dialogue lines
        """
        # Use LLM for advanced dialogue if requested and available
        if self.use_llm and use_advanced:
            return self._generate_advanced_dialogue(
                speaker=character1,
                listener=character2,
                context=context,
                style=style,
                num_lines=num_lines,
                **kwargs
            )
        
        # Fall back to template-based dialogue
        return self._generate_template_dialogue(character1, character2, context, num_lines)
    
    def _generate_advanced_dialogue(self, 
                                   speaker: str, 
                                   listener: str, 
                                   context: str,
                                   style: str = "natural",
                                   num_lines: int = 5,
                                   **kwargs) -> List[str]:
        """Generate dialogue using LLM backend"""
        if not self.llm_backend:
            return self._generate_template_dialogue(speaker, listener, context, num_lines)
        
        try:
            return self.llm_backend.generate_dialogue(
                speaker=speaker,
                listener=listener,
                context=context,
                style=style,
                num_lines=num_lines,
                **kwargs
            )
        except Exception as e:
            print(f"Warning: LLM dialogue failed: {e}. Using templates.")
            return self._generate_template_dialogue(speaker, listener, context, num_lines)
    
    def _generate_template_dialogue(self, 
                                   character1: str, 
                                   character2: str, 
                                   context: str, 
                                   num_lines: int) -> List[str]:
        """Generate dialogue using template patterns"""
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
                                 scene_purpose: str,
                                 use_advanced: bool = False) -> Dict:
        """Create a complete conversation scene"""
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
        
        # Generate dialogue
        if len(characters) >= 2:
            scene["dialogue"] = self.generate_dialogue(
                characters[0].get("name", "Character A"),
                characters[1].get("name", "Character B"),
                context=scene_purpose,
                use_advanced=use_advanced
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
                          mood: str = "reflective",
                          use_advanced: bool = False) -> List[str]:
        """Generate a character monologue"""
        
        if self.use_llm and use_advanced:
            try:
                prompt = f"Write a {mood} monologue from {character} about {topic}."
                response = self.llm_backend.generate(prompt, max_tokens=200)
                lines = [f"{character}: {line.strip()}" for line in response.split('\n') if line.strip()]
                if lines:
                    return lines[:8]
            except Exception:
                pass
        
        # Template monologues
        monologues = {
            "reflective": [
                f"{character}: You know, I've been thinking about {topic}...",
                f"{character}: It's strange how things turn out sometimes.",
                f"{character}: I never expected to find myself here.",
                f"{character}: Everything makes sense. And nothing makes sense."
            ],
            "determined": [
                f"{character}: I've come too far to give up now.",
                f"{character}: {topic} is all that matters.",
                f"{character}: They can try to stop me, but they don't understand.",
                f"{character}: I will succeed. I have to."
            ]
        }
        
        return monologues.get(mood, monologues["reflective"])
    
    def has_llm(self) -> bool:
        """Check if LLM backend is available"""
        return self.use_llm
    
    def get_llm_info(self) -> Dict:
        """Get information about LLM backend"""
        if self.use_llm and hasattr(self.llm_backend, 'config'):
            return {
                "available": True,
                "provider": self.llm_backend.config.provider.value,
                "model": self.llm_backend.config.model
            }
        return {"available": False}
    
    def __str__(self) -> str:
        status = "with LLM" if self.use_llm else "template-based"
        return f"DialogueGenerator({status})"