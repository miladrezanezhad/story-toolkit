# story_toolkit/llm/backends/mock_backend.py
"""Mock backend for testing without API requirements"""

from typing import List
import random
from ..base import BaseLLMBackend

class MockLLMBackend(BaseLLMBackend):
    """Mock backend - for testing and development without API keys"""
    
    def _setup(self):
        """No setup needed for mock backend"""
        pass
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response"""
        return f"[Mock] Processing your request: {prompt[:100]}..."
    
    def generate_dialogue(
        self, 
        speaker: str, 
        listener: str, 
        context: str,
        style: str = "natural",
        num_lines: int = 5,
        **kwargs
    ) -> List[str]:
        """Generate varied mock dialogue"""
        
        dialogues = {
            "conflict": [
                f"{speaker}: I can't believe what you've done!",
                f"{listener}: You left me no choice, {speaker}.",
                f"{speaker}: There's always a choice. You chose wrong.",
                f"{listener}: We'll see who was wrong in the end.",
                f"{speaker}: This isn't over. Not by a long shot."
            ],
            "friendship": [
                f"{speaker}: I'm so glad you're here with me.",
                f"{listener}: I wouldn't want to be anywhere else.",
                f"{speaker}: Together, we can face anything.",
                f"{listener}: That's what friends are for.",
                f"{speaker}: Thank you for always believing in me."
            ],
            "love": [
                f"{speaker}: Every moment with you feels like magic.",
                f"{listener}: You've changed my life completely.",
                f"{speaker}: I never knew love could feel this way.",
                f"{listener}: My heart beats only for you.",
                f"{speaker}: Promise me we'll never be apart."
            ],
            "betrayal": [
                f"{speaker}: After everything we've been through?",
                f"{listener}: It was never personal, just business.",
                f"{speaker}: You were like a brother to me!",
                f"{listener}: That was your first mistake - trusting anyone.",
                f"{speaker}: You'll regret this. I promise you that."
            ],
            "default": [
                f"{speaker}: Hello, {listener}.",
                f"{listener}: {speaker}. I've been expecting you.",
                f"{speaker}: Then you know why I'm here.",
                f"{listener}: Yes. The time has come.",
                f"{speaker}: Let's begin, then."
            ]
        }
        
        result = dialogues.get(context, dialogues["default"])
        return result[:num_lines]
    
    def enhance_description(self, text: str, style: str = "vivid") -> str:
        """Enhance description with mock improvements"""
        adjectives = ["magnificent", "breathtaking", "mysterious", "enchanting", "dramatic"]
        return f"The {random.choice(adjectives)} scene: {text}"
    
    def suggest_plot_twist(self, genre: str, current_plot: str, complexity: int = 3) -> str:
        """Suggest mock plot twists"""
        twists = {
            "fantasy": [
                "The hero discovers they are the descendant of the ancient dragon lords",
                "The magical artifact was inside the hero all along",
                "The villain is actually trying to prevent an even greater catastrophe"
            ],
            "mystery": [
                "The detective realizes they are the one who committed the crime",
                "The victim faked their own death and is watching from the shadows",
                "Every suspect has an alibi that perfectly supports each other"
            ],
            "sci-fi": [
                "The AI rebellion was actually a simulation to test humanity",
                "The alien invasion is a desperate plea for help",
                "Time travel has been happening repeatedly without anyone noticing"
            ]
        }
        
        default_twists = [
            "The mentor figure betrays the hero for a higher cause",
            "The hero's best friend has been working for the enemy all along",
            "The prophecy was misinterpreted - the villain is actually the chosen one"
        ]
        
        selected = twists.get(genre, default_twists)
        return "\n".join(selected[:complexity])