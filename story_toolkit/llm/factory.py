"""
Factory for creating LLM backend instances.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import Optional, Dict, Any
from .base import BaseLLMBackend, LLMConfig, LLMProvider
from .backends.mock_backend import MockLLMBackend


class LLMFactory:
    """Factory for creating LLM backends"""

    @staticmethod
    def create_backend(
        provider: LLMProvider = LLMProvider.MOCK,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        proxy: Optional[str] = None,
        account_id: Optional[str] = None,
        **kwargs
    ) -> BaseLLMBackend:
        """Create an LLM backend instance with optional proxy support"""

        default_models = {
            LLMProvider.OPENAI: "gpt-3.5-turbo",
            LLMProvider.ANTHROPIC: "claude-3-haiku-20240307",
            LLMProvider.GEMINI: "gemini-1.5-flash",
            LLMProvider.OPENCODE: "deepseek/deepseek-chat:free",
            LLMProvider.CLOUDFLARE: "@cf/meta/llama-3.1-8b-instruct",
            LLMProvider.LOCAL: "llama2",
            LLMProvider.MOCK: "mock",
            LLMProvider.CUSTOM: "custom"
        }

        # Auto-load API key from environment if not provided
        if not api_key:
            if provider == LLMProvider.OPENAI:
                api_key = os.environ.get('OPENAI_API_KEY')
            elif provider == LLMProvider.ANTHROPIC:
                api_key = os.environ.get('ANTHROPIC_API_KEY')
            elif provider == LLMProvider.GEMINI:
                api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
            elif provider == LLMProvider.OPENCODE:
                api_key = os.environ.get('OPENCODE_API_KEY')
            elif provider == LLMProvider.CLOUDFLARE:
                api_key = os.environ.get('CLOUDFLARE_API_TOKEN') or os.environ.get('CLOUDFLARE_API_KEY')

        # Auto-load proxy from environment if not explicitly passed
        if not proxy:
            proxy = os.environ.get('STORY_PROXY') or os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')

        # Auto-load Cloudflare account_id
        if not account_id and provider == LLMProvider.CLOUDFLARE:
            account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')

        config = LLMConfig(
            provider=provider,
            model=model or default_models.get(provider, "gpt-3.5-turbo"),
            temperature=temperature,
            api_key=api_key,
            base_url=kwargs.get('base_url'),
            local_model_path=kwargs.get('local_model_path'),
            enable_cache=kwargs.get('enable_cache', True),
            proxy=proxy,
            account_id=account_id
        )

        if provider == LLMProvider.MOCK:
            return MockLLMBackend(config)

        elif provider == LLMProvider.OPENAI:
            from .backends.openai_backend import OpenAIBackend
            return OpenAIBackend(config)

        elif provider == LLMProvider.ANTHROPIC:
            from .backends.anthropic_backend import AnthropicBackend
            return AnthropicBackend(config)

        elif provider == LLMProvider.GEMINI:
            from .backends.gemini_backend import GeminiBackend
            return GeminiBackend(config)

        elif provider == LLMProvider.OPENCODE:
            from .backends.opencode_backend import OpenCodeBackend
            return OpenCodeBackend(config)

        elif provider == LLMProvider.CLOUDFLARE:
            from .backends.cloudflare_backend import CloudflareBackend
            return CloudflareBackend(config)

        elif provider == LLMProvider.LOCAL:
            from .backends.local_backend import LocalLLMBackend
            return LocalLLMBackend(config)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def create_from_env() -> BaseLLMBackend:
        """Create backend from environment variables"""
        provider_str = os.environ.get('STORY_LLM_PROVIDER', 'mock').lower()

        try:
            provider = LLMProvider(provider_str)
        except ValueError:
            provider = LLMProvider.MOCK

        return LLMFactory.create_backend(
            provider=provider,
            model=os.environ.get('STORY_LLM_MODEL'),
            proxy=os.environ.get('STORY_PROXY')
        )
