# story_toolkit/llm/backends/openai_backend.py
"""OpenAI backend - Support for GPT-4, GPT-3.5"""

from typing import List
from ..base import BaseLLMBackend

class OpenAIBackend(BaseLLMBackend):
    """OpenAI backend for GPT model access"""
    
    def _setup(self):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
    
    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call OpenAI API"""
        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a professional storyteller and creative writer. Respond in the same language as the user."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get('temperature', self.config.temperature),
                max_tokens=kwargs.get('max_tokens', self.config.max_tokens)
            )
            result = response.choices[0].message.content
            self._set_cache(cache_key, result)
            return result
        except Exception as e:
            return f"[OpenAI Error: {str(e)}]"
    
    def generate(self, prompt: str, **kwargs) -> str:
        return self._call_api(prompt, **kwargs)
    
    def generate_dialogue(
        self, 
        speaker: str, 
        listener: str, 
        context: str,
        style: str = "natural",
        num_lines: int = 5,
        **kwargs
    ) -> List[str]:
        """Generate advanced dialogue using OpenAI"""
        
        prompt = f"""Generate a {style} dialogue between '{speaker}' and '{listener}' in a '{context}' context.

Requirements:
- Write exactly {num_lines} lines of dialogue
- Each line must start with the character name followed by colon (e.g., "{speaker}: text")
- Make the dialogue emotional, natural, and believable
- Avoid clichés
- Show the relationship dynamic between characters

Dialogue:"""
        
        response = self._call_api(prompt, **kwargs)
        
        # Parse response into lines
        lines = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and ':' in line:
                lines.append(line)
            elif line and lines:  # Continuation of previous line
                lines[-1] = lines[-1] + " " + line
        
        return lines[:num_lines]
    
    def enhance_description(self, text: str, style: str = "vivid") -> str:
        """Enhance descriptive text with GPT"""
        prompt = f"""Enhance this descriptive text to be more {style} and engaging.
Keep the same meaning and information, just improve the language and imagery.

Original: {text}

Enhanced version:"""
        
        return self._call_api(prompt, max_tokens=200)
    
    def suggest_plot_twist(self, genre: str, current_plot: str, complexity: int = 3) -> str:
        """Suggest plot twists using GPT"""
        prompt = f"""Genre: {genre}
Current plot summary: {current_plot}
Complexity level (1-5): {complexity}

Suggest {complexity} creative, unexpected but logical plot twists.
Format as a numbered list.

Plot twists:"""
        
        return self._call_api(prompt, max_tokens=400)
