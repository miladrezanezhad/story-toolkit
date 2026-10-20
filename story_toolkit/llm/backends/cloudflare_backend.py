"""
Cloudflare Workers AI backend for Story Toolkit.
Support for Cloudflare Workers AI models (Llama 3.1, Llama 3.3, DeepSeek R1, Mistral, Qwen).
Full proxy support.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import List, Optional
from ..base import BaseLLMBackend


class CloudflareBackend(BaseLLMBackend):
    """Cloudflare Workers AI backend"""

    def _setup(self):
        if not self.config.model or self.config.model in ["cloudflare", "default"]:
            self.config.model = "@cf/meta/llama-3.1-8b-instruct"

        if not self.config.account_id:
            self.config.account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')

    def _call_api(self, prompt: str, **kwargs) -> str:
        """Call Cloudflare Workers AI endpoint"""
        if not self.config.api_key:
            return "[Cloudflare Error: API Token is not configured. Add your Cloudflare API token in Settings.]"

        account_id = self.config.account_id or os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')
        if not account_id:
            return "[Cloudflare Error: Account ID is required. Please set your Cloudflare Account ID in Settings or CLOUDFLARE_ACCOUNT_ID env.]"

        cache_key = f"{prompt}_{kwargs.get('temperature', self.config.temperature)}_{self.config.model}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        model = kwargs.get('model', self.config.model)
        # Ensure model has @cf/ prefix if needed
        if not model.startswith("@cf/") and not model.startswith("@hf/"):
            model = f"@cf/{model}"

        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"

        headers = {
            "Authorization": f"Bearer {self.config.api_key}"
        }

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional author and creative narrative assistant. Respond in the same language as the user."
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": kwargs.get('max_tokens', self.config.max_tokens),
            "temperature": kwargs.get('temperature', self.config.temperature)
        }

        try:
            res_json = self._make_http_request(url, payload, headers=headers)

            # Cloudflare standard return: {"result": {"response": "..."}, "success": true}
            if res_json.get("success") and "result" in res_json:
                result = res_json["result"].get("response", "")
                self._set_cache(cache_key, result)
                return result

            # Check alternative format
            if "choices" in res_json:
                result = res_json["choices"][0].get("message", {}).get("content", "")
                self._set_cache(cache_key, result)
                return result

            if "errors" in res_json and res_json["errors"]:
                err_msg = res_json["errors"][0].get("message", "Unknown error")
                return f"[Cloudflare Error: {err_msg}]"

            return f"[Cloudflare Error: Unexpected response {res_json}]"
        except Exception as e:
            return f"[Cloudflare Request Error: {str(e)}]"

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
Make it authentic, dramatic, and engaging.

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
