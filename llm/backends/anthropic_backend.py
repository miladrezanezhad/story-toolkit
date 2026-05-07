# story_toolkit/llm/backends/anthropic_backend.py
"""Anthropic backend - Support for Claude models"""

from typing import List
from ..base import BaseLLMBackend

class AnthropicBackend(BaseLLMBackend):
    """Anthropic backend for Claude model access"""
    
    def _setup(self):
        from anthropic import Anthropic
        self.client = Anthropic(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
    
    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call Anthropic API"""
        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=kwargs.get('max_tokens', self.config.max_tokens),
                temperature=kwargs.get('temperature', self.config.temperature),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.content[0].text
            self._set_cache(cache_key, result)
            return result
        except Exception as e:
            return f"[Anthropic Error: {str(e)}]"
    
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
        prompt = f"""Generate a {style} dialogue between '{speaker}' and '{listener}' in a '{context}' context.
Write exactly {num_lines} lines in format "speaker: text".
Make it emotional and natural.

Dialogue:"""
        
        response = self._call_api(prompt, **kwargs)
        
        lines = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and ':' in line:
                lines.append(line)
        
        return lines[:num_lines]
