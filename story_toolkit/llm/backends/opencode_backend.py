"""
OpenCode Free API backend for Story Toolkit.
Support for free open-source models (DeepSeek, Llama 3.1, Qwen, Mistral).
Compatible with OpenCode and OpenAI-compatible free providers with full proxy support.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List, Optional
from ..base import BaseLLMBackend


class OpenCodeBackend(BaseLLMBackend):
    """OpenCode Free backend for open-source AI models"""

    def _setup(self):
        if not self.config.base_url:
            self.config.base_url = "https://api.opencode.com/v1"
        if not self.config.model or self.config.model in ["opencode", "default"]:
            self.config.model = "deepseek/deepseek-chat:free"

    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call OpenCode Free chat completions endpoint"""
        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}_{self.config.model}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        base_url = (self.config.base_url or "https://api.opencode.com/v1").rstrip('/')
        url = f"{base_url}/chat/completions"

        headers = {}
        api_key = self.config.api_key or "free"
        headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": kwargs.get('model', self.config.model),
            "messages": [
                {
                    "role": "system",
                    "content": "You are a creative writer and storyteller. Respond in the same language as the user."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get('temperature', self.config.temperature),
            "max_tokens": kwargs.get('max_tokens', self.config.max_tokens)
        }

        try:
            res_json = self._make_http_request(url, payload, headers=headers)
            choices = res_json.get("choices", [])
            if choices:
                result = choices[0].get("message", {}).get("content", "")
                self._set_cache(cache_key, result)
                return result

            if "error" in res_json:
                return f"[OpenCode Error: {res_json['error']}]"

            return f"[OpenCode Error: Unexpected response {res_json}]"
        except Exception as e:
            return f"[OpenCode Request Error: {str(e)}]"

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
Write exactly {num_lines} lines of dialogue in format "{speaker}: text".
Make it authentic, emotional, and engaging.

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
