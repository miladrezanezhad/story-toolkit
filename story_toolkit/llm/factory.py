"""
Factory for creating LLM backend instances.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import Optional
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
        **kwargs
    ) -> BaseLLMBackend:
        """Create an LLM backend instance"""
        
        default_models = {
            LLMProvider.OPENAI: "gpt-3.5-turbo",
            LLMProvider.ANTHROPIC: "claude-3-haiku-20240307",
            LLMProvider.LOCAL: "llama2",
            LLMProvider.MOCK: "mock",
        }
        
        config = LLMConfig(
            provider=provider,
            model=model or default_models.get(provider, "gpt-3.5-turbo"),
            temperature=temperature,
            api_key=api_key,
            base_url=kwargs.get('base_url'),
            local_model_path=kwargs.get('local_model_path'),
            enable_cache=kwargs.get('enable_cache', True)
        )
        
        if provider == LLMProvider.MOCK:
            return MockLLMBackend(config)
        
        # For now, only mock is implemented
        # OpenAI, Anthropic, Local can be added later
        raise ValueError(f"Provider {provider} not yet implemented. Use MOCK for testing.")
    
    @staticmethod
    def create_from_env() -> BaseLLMBackend:
        """Create backend from environment variables"""
        import os
        
        provider_str = os.environ.get('STORY_LLM_PROVIDER', 'mock')
        
        try:
            provider = LLMProvider(provider_str)
        except ValueError:
            provider = LLMProvider.MOCK
        
        return LLMFactory.create_backend(provider=provider)
