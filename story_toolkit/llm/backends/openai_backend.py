"""
OpenAI backend for Story Toolkit.
Support for GPT-4, GPT-3.5, and other OpenAI models with full proxy support.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import List, Optional
from ..base import BaseLLMBackend


class OpenAIBackend(BaseLLMBackend):
    """OpenAI backend for GPT model access with proxy support"""

    def _setup(self):
        # Configure proxy in environment if present
        if self.config.proxy and self.config.proxy.strip():
            os.environ["HTTP_PROXY"] = self.config.proxy.strip()
            os.environ["HTTPS_PROXY"] = self.config.proxy.strip()

        try:
            from openai import OpenAI
            client_kwargs = {
                "api_key": self.config.api_key,
                "base_url": self.config.base_url,
                "timeout": self.config.timeout
            }
            if self.config.proxy and self.config.proxy.strip():
                try:
                    import httpx
                    client_kwargs["http_client"] = httpx.Client(proxy=self.config.proxy.strip())
                except ImportError:
                    pass

            self.client = OpenAI(**client_kwargs)
        except ImportError:
            self.client = None

    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call OpenAI API (via client or direct REST with proxy)"""
        if not self.config.api_key:
            return "[OpenAI Error: API key is not configured. Please add your OpenAI API key in Settings.]"

        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}_{self.config.model}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # Try client first if available
        if self.client is not None:
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional storyteller and creative writer. Respond in the same language as the user."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=kwargs.get('temperature', self.config.temperature),
                    max_tokens=kwargs.get('max_tokens', self.config.max_tokens)
                )
                result = response.choices[0].message.content
                self._set_cache(cache_key, result)
                return result
            except Exception as e:
                # If SDK fails or proxy issues, fall back to direct HTTP
                pass

        # Direct HTTP fallback with proxy
        base_url = (self.config.base_url or "https://api.openai.com/v1").rstrip('/')
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}"
        }
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional storyteller and creative writer. Respond in the same language as the user."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get('temperature', self.config.temperature),
            "max_tokens": kwargs.get('max_tokens', self.config.max_tokens)
        }

        try:
            res_json = self._make_http_request(url, payload, headers=headers)
            if "choices" in res_json and res_json["choices"]:
                result = res_json["choices"][0].get("message", {}).get("content", "")
                self._set_cache(cache_key, result)
                return result
            if "error" in res_json:
                return f"[OpenAI Error: {res_json['error'].get('message', 'Unknown error')}]"
            return f"[OpenAI Error: Unexpected response {res_json}]"
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
        prompt = f"""Enhance this descriptive text to be more {style} and engaging.
Keep the same meaning and information, just improve the language and imagery.

Original: {text}

Enhanced version:"""
        return self._call_api(prompt, max_tokens=200)

    def suggest_plot_twist(self, genre: str, current_plot: str, complexity: int = 3) -> str:
        prompt = f"""Genre: {genre}
Current plot summary: {current_plot}
Complexity level (1-5): {complexity}

Suggest {complexity} creative, unexpected but logical plot twists.
Format as a numbered list.

Plot twists:"""
        return self._call_api(prompt, max_tokens=400)
