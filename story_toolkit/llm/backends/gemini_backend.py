"""
Google Gemini backend for Story Toolkit.
Support for Gemini 2.0 Flash, Gemini 1.5 Flash, Gemini 1.5 Pro.
Works with proxy support out-of-the-box.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List, Optional
from ..base import BaseLLMBackend


class GeminiBackend(BaseLLMBackend):
    """Google Gemini backend for creative story generation"""

    def _setup(self):
        # Default model if not specified or placeholder
        if not self.config.model or self.config.model in ["gemini", "default"]:
            self.config.model = "gemini-1.5-flash"

    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call Gemini REST API with proxy support"""
        if not self.config.api_key:
            return "[Gemini Error: API key is not configured. Add your Google Gemini API key in Settings.]"

        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}_{self.config.model}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        model = kwargs.get('model', self.config.model)
        # Ensure model has no prefix
        if model.startswith("models/"):
            model = model.replace("models/", "")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.config.api_key}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": kwargs.get('temperature', self.config.temperature),
                "maxOutputTokens": kwargs.get('max_tokens', self.config.max_tokens)
            }
        }

        try:
            res_json = self._make_http_request(url, payload)
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    result = parts[0].get("text", "")
                    self._set_cache(cache_key, result)
                    return result

            # If error returned in JSON
            if "error" in res_json:
                return f"[Gemini Error: {res_json['error'].get('message', 'Unknown error')}]"

            return f"[Gemini Error: Unexpected response format: {res_json}]"
        except Exception as e:
            return f"[Gemini Request Error: {str(e)}]"

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

Requirements:
- Write exactly {num_lines} lines of dialogue
- Each line must start with the character name followed by colon (e.g. "{speaker}: text")
- Make the dialogue emotional, natural, and engaging
- Show character personality and relationship dynamics

Dialogue:"""

        response = self._call_api(prompt, **kwargs)

        lines = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and ':' in line:
                lines.append(line)
            elif line and lines:
                lines[-1] = lines[-1] + " " + line

        if not lines:
            from .mock_backend import MockLLMBackend
            return MockLLMBackend(self.config).generate_dialogue(speaker, listener, context, style, num_lines)

        return lines[:num_lines]

    def enhance_description(self, text: str, style: str = "vivid") -> str:
        prompt = f"Enhance and enrich this descriptive story scene in {style} narrative style. Keep meaning intact:\n\n{text}"
        return self._call_api(prompt)

    def suggest_plot_twist(self, genre: str, current_plot: str, complexity: int = 3) -> str:
        prompt = f"Genre: {genre}\nCurrent plot summary: {current_plot}\n\nSuggest {complexity} unexpected, logical plot twists."
        return self._call_api(prompt)
