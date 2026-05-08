"""
Dialogue Generator Module
=========================
Generates natural-sounding dialogues between characters.
Now supports optional LLM integration for advanced dialogue generation.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import random
from typing import List, Dict, Optional, Union, Any

# Optional LLM import - if llm module exists
try:
    from ..llm import BaseLLMBackend
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    # Define a dummy type for type hints
    BaseLLMBackend = Any


class DialogueGenerator:
    """Generates dialogues for various story contexts with optional LLM support"""
    
    def __init__(self, llm_backend: Optional[BaseLLMBackend] = None):
        """
        Initialize the Dialogue Generator.
        
        Args:
            llm_backend: Optional LLM backend for advanced dialogue generation
        """
        self.llm_backend = llm_backend
        self.use_llm = llm_backend is not None and LLM_AVAILABLE
        
        # Dialogue templates for different contexts (legacy/backup)
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
            ],
            "default": [
                [
                    "{char1}: Hello {char2}.",
                    "{char2}: {char1}. I've been expecting you.",
                    "{char1}: Then you know why I'm here."
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
        
    def generate_dialogue(self, 
                         character1: str, 
                         character2: str,
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
            context: Dialogue context (conflict, revelation, emotional, romantic, mysterious)
            mood: Emotional mood of the dialogue
            num_lines: Number of dialogue lines to generate
            use_advanced: Use LLM for advanced dialogue generation if available
            style: Dialogue style for advanced generation (natural, dramatic, poetic, humorous)
            **kwargs: Additional parameters passed to LLM backend
            
        Returns:
            List of dialogue lines
        """
        # Use LLM for advanced dialogue if requested and available
        if self.use_llm and use_advanced:
            try:
                return self._generate_advanced_dialogue(
                    speaker=character1,
                    listener=character2,
                    context=context,
                    style=style,
                    num_lines=num_lines,
                    **kwargs
                )
            except Exception as e:
                # If advanced fails, fall back silently
                print(f"Debug: LLM dialogue failed ({e}), using templates")
                return self._generate_template_dialogue(character1, character2, context, num_lines)
        
        # Fall back to template-based dialogue (legacy mode)
        return self._generate_template_dialogue(character1, character2, context, num_lines)
    
    def _generate_advanced_dialogue(self, 
                                   speaker: str, 
                                   listener: str, 
                                   context: str,
                                   style: str = "natural",
                                   num_lines: int = 5,
                                   **kwargs) -> List[str]:
        """
        Generate dialogue using LLM backend.
        
        Args:
            speaker: Speaker's name
            listener: Listener's name
            context: Dialogue context
            style: Dialogue style
            num_lines: Number of lines
            **kwargs: Additional LLM parameters
            
        Returns:
            List of dialogue lines
        """
        if not self.llm_backend:
            # If no LLM backend, fall back to template
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
        except AttributeError:
            # If generate_dialogue method doesn't exist, try generate method
            try:
                prompt = f"Generate a {style} dialogue between {speaker} and {listener} in {context} context. Write {num_lines} lines in format 'name: text'."
                response = self.llm_backend.generate(prompt, **kwargs)
                lines = []
                for line in response.strip().split('\n'):
                    if ':' in line:
                        lines.append(line.strip())
                return lines[:num_lines] if lines else self._generate_template_dialogue(speaker, listener, context, num_lines)
            except Exception:
                return self._generate_template_dialogue(speaker, listener, context, num_lines)
        except Exception as e:
            # Log error and fall back to template
            print(f"Warning: LLM dialogue generation failed: {e}. Falling back to templates.")
            return self._generate_template_dialogue(speaker, listener, context, num_lines)
    
    def _generate_template_dialogue(self, 
                                   character1: str, 
                                   character2: str, 
                                   context: str, 
                                   num_lines: int) -> List[str]:
        """
        Generate dialogue using template patterns (legacy method).
        
        Args:
            character1: Name of first character
            character2: Name of second character
            context: Dialogue context
            num_lines: Number of lines
            
        Returns:
            List of dialogue lines
        """
        # Default context handling
        context_key = context if context in self.dialogue_patterns else "default"
        template = random.choice(self.dialogue_patterns[context_key])
        dialogue = []
        
        for line in template[:num_lines]:
            formatted_line = line.format(
                char1=character1,
                char2=character2
            )
            dialogue.append(formatted_line)
        
        # If we need more lines than template provides, repeat with modifications
        while len(dialogue) < num_lines:
            extra_line = f"{character1}: We need to continue this conversation..."
            dialogue.append(extra_line)
        
        return dialogue[:num_lines]
    
    def create_conversation_scene(self, characters: List[Dict],
                                 scene_purpose: str,
                                 use_advanced: bool = False) -> Dict:
        """
        Create a complete conversation scene.
        
        Args:
            characters: List of character dictionaries
            scene_purpose: Purpose of the scene (confrontation, confession, romantic, etc.)
            use_advanced: Use LLM for advanced dialogue generation
            
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
        
        # Generate dialogue
        if len(characters) >= 2:
            scene["dialogue"] = self.generate_dialogue(
                characters[0].get("name", "Character A"),
                characters[1].get("name", "Character B"),
                context=scene_purpose,
                use_advanced=use_advanced,
                num_lines=5
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
        """
        Generate a character monologue.
        
        Args:
            character: Character name
            topic: Monologue topic
            mood: Emotional mood (reflective, determined, sad, hopeful)
            use_advanced: Use LLM for advanced monologue generation
            
        Returns:
            List of monologue lines
        """
        # Use advanced generation if available and requested
        if self.use_llm and use_advanced:
            try:
                prompt = f"Write a {mood} monologue from {character} about {topic}. Keep it concise and emotional. Write 4-6 lines."
                response = self.llm_backend.generate(prompt, max_tokens=300)
                # Split into lines
                lines = [f"{character}: {line.strip()}" for line in response.split('\n') if line.strip()]
                if lines:
                    return lines[:8]
            except Exception as e:
                print(f"Debug: LLM monologue failed ({e}), using templates")
        
        # Fall back to template monologues
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
            ],
            "sad": [
                f"{character}: {topic}... it's all I think about.",
                f"{character}: Sometimes I wonder if things could have been different.",
                f"{character}: But what's done is done. I can't change the past.",
                f"{character}: I can only learn to live with it."
            ],
            "hopeful": [
                f"{character}: Maybe {topic} is exactly what I needed.",
                f"{character}: There's a light at the end of this tunnel.",
                f"{character}: Tomorrow is a new day. A new beginning.",
                f"{character}: And I'm ready for whatever comes."
            ]
        }
        
        return monologues.get(mood, monologues["reflective"])
    
    def has_llm(self) -> bool:
        """Check if LLM backend is available"""
        return self.use_llm and self.llm_backend is not None
    
    def get_llm_info(self) -> Dict:
        """Get information about the LLM backend if available"""
        if self.use_llm and hasattr(self.llm_backend, 'config'):
            return {
                "available": True,
                "provider": getattr(self.llm_backend.config, 'provider', 'unknown'),
                "model": getattr(self.llm_backend.config, 'model', 'unknown')
            }
        return {"available": False}
    
    def __str__(self) -> str:
        llm_status = "with LLM" if self.use_llm else "template-based"
        return f"DialogueGenerator({llm_status}, contexts={len(self.dialogue_patterns)})"