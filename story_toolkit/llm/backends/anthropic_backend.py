"""
Anthropic backend for Story Toolkit.
Support for Claude models (Claude 3.5 Sonnet, Claude 3 Haiku, Claude 3 Opus) with proxy support.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import List, Optional
from ..base import BaseLLMBackend


class AnthropicBackend(BaseLLMBackend):
    """Anthropic backend for Claude model access with proxy support"""

    def _setup(self):
        # Configure proxy in environment if present
        if self.config.proxy and self.config.proxy.strip():
            os.environ["HTTP_PROXY"] = self.config.proxy.strip()
            os.environ["HTTPS_PROXY"] = self.config.proxy.strip()

        try:
            from anthropic import Anthropic
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

            self.client = Anthropic(**client_kwargs)
        except ImportError:
            self.client = None

    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call Anthropic API (via client or direct REST with proxy)"""
        if not self.config.api_key:
            return "[Anthropic Error: API key is not configured. Please add your Anthropic API key in Settings.]"

        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}_{self.config.model}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        if self.client is not None:
            try:
                response = self.client.messages.create(
                    model=self.config.model,
                    max_tokens=kwargs.get('max_tokens', self.config.max_tokens),
                    temperature=kwargs.get('temperature', self.config.temperature),
                    system="You are an expert storyteller, novelist, and creative narrative assistant.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.content[0].text
                self._set_cache(cache_key, result)
                return result
            except Exception as e:
                pass

        # Fallback to direct HTTP with proxy
        base_url = (self.config.base_url or "https://api.anthropic.com").rstrip('/')
        url = f"{base_url}/v1/messages"
        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": self.config.model,
            "max_tokens": kwargs.get('max_tokens', self.config.max_tokens),
            "temperature": kwargs.get('temperature', self.config.temperature),
            "system": "You are an expert storyteller, novelist, and creative narrative assistant.",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            res_json = self._make_http_request(url, payload, headers=headers)
            content = res_json.get("content", [])
            if content and "text" in content[0]:
                result = content[0]["text"]
                self._set_cache(cache_key, result)
                return result
            if "error" in res_json:
                return f"[Anthropic Error: {res_json['error'].get('message', 'Unknown error')}]"
            return f"[Anthropic Error: Unexpected response {res_json}]"
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
Write exactly {num_lines} lines in format "{speaker}: text".
Make it emotional, natural, and character-driven.

Dialogue:"""

        response = self._call_api(prompt, **kwargs)

        lines = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and ':' in line:
                lines.append(line)

        if not lines:
            from .mock_backend import MockLLMBackend
            return MockLLMBackend(self.config).generate_dialogue(speaker, listener, context, style, num_lines)

        return lines[:num_lines]
