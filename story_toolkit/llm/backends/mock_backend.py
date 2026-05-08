"""
Mock LLM backend for testing without API keys.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List
import random
from ..base import BaseLLMBackend


class MockLLMBackend(BaseLLMBackend):
    """Mock backend for testing - no API required"""
    
    def _setup(self):
        """No setup needed for mock"""
        pass
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response"""
        return f"[Mock] Processing: {prompt[:100]}..."
    
    def generate_dialogue(
        self, 
        speaker: str, 
        listener: str, 
        context: str,
        style: str = "natural",
        num_lines: int = 5,
        **kwargs
    ) -> List[str]:
        """Generate mock dialogue"""
        
        dialogues = {
            "conflict": [
                f"{speaker}: I can't believe what you've done!",
                f"{listener}: You left me no choice, {speaker}.",
                f"{speaker}: There's always a choice. You chose wrong.",
                f"{listener}: We'll see who was wrong in the end.",
                f"{speaker}: This isn't over."
            ],
            "friendship": [
                f"{speaker}: I'm glad you're here with me.",
                f"{listener}: I wouldn't want to be anywhere else.",
                f"{speaker}: Together, we can face anything.",
                f"{listener}: That's what friends are for.",
                f"{speaker}: Thank you for believing in me."
            ],
            "love": [
                f"{speaker}: Every moment with you feels like magic.",
                f"{listener}: You've changed my life completely.",
                f"{speaker}: I never knew love could feel this way.",
                f"{listener}: My heart beats only for you.",
                f"{speaker}: Promise me we'll never be apart."
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