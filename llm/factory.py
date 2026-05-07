# story_toolkit/llm/factory.py
"""Factory for creating LLM backends"""

from typing import Optional, Dict, Any
from .base import BaseLLMBackend, LLMConfig, LLMProvider
from .backends.mock_backend import MockLLMBackend

class LLMFactory:
    """Factory class for creating LLM backends"""
    
    @staticmethod
    def create_backend(
        provider: LLMProvider = LLMProvider.MOCK,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> BaseLLMBackend:
        """Create an LLM backend instance
        
        Args:
            provider: Type of provider (openai, anthropic, local, mock)
            api_key: API key (for OpenAI/Anthropic)
            model: Model name (default depends on provider)
            temperature: Creativity level (0 to 1)
            
        Returns:
            Instance of selected backend
            
        Examples:
            >>> # Use OpenAI
            >>> llm = LLMFactory.create_backend(
            ...     provider=LLMProvider.OPENAI,
            ...     api_key="sk-...",
            ...     model="gpt-4"
            ... )
            
            >>> # Use Local (Ollama)
            >>> llm = LLMFactory.create_backend(
            ...     provider=LLMProvider.LOCAL,
            ...     model="llama2"
            ... )
        """
        
        # Default model configurations
        default_models = {
            LLMProvider.OPENAI: "gpt-3.5-turbo",
            LLMProvider.ANTHROPIC: "claude-3-haiku-20240307",
            LLMProvider.LOCAL: "llama2",
            LLMProvider.MOCK: "mock",
            LLMProvider.CUSTOM: "custom"
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
        
        # Select appropriate backend
        if provider == LLMProvider.MOCK:
            return MockLLMBackend(config)
        
        elif provider == LLMProvider.OPENAI:
            try:
                from .backends.openai_backend import OpenAIBackend
                return OpenAIBackend(config)
            except ImportError:
                raise ImportError(
                    "OpenAI backend requires `openai` package. "
                    "Install with: pip install openai"
                )
        
        elif provider == LLMProvider.ANTHROPIC:
            try:
                from .backends.anthropic_backend import AnthropicBackend
                return AnthropicBackend(config)
            except ImportError:
                raise ImportError(
                    "Anthropic backend requires `anthropic` package. "
                    "Install with: pip install anthropic"
                )
        
        elif provider == LLMProvider.LOCAL:
            try:
                from .backends.local_backend import LocalLLMBackend
                return LocalLLMBackend(config)
            except ImportError:
                raise ImportError(
                    "Local backend requires `ollama` or `llama-cpp-python`. "
                    "Install with: pip install ollama"
                )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    def create_from_env() -> BaseLLMBackend:
        """Create backend from environment variables
        
        Supported environment variables:
            - STORY_LLM_PROVIDER: openai, anthropic, local
            - OPENAI_API_KEY: OpenAI API key
            - ANTHROPIC_API_KEY: Anthropic API key
            - STORY_LLM_MODEL: Model name
        """
        import os
        
        provider_str = os.environ.get('STORY_LLM_PROVIDER', 'mock')
        
        try:
            provider = LLMProvider(provider_str)
        except ValueError:
            provider = LLMProvider.MOCK
        
        api_key = None
        if provider == LLMProvider.OPENAI:
            api_key = os.environ.get('OPENAI_API_KEY')
        elif provider == LLMProvider.ANTHROPIC:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        return LLMFactory.create_backend(
            provider=provider,
            api_key=api_key,
            model=os.environ.get('STORY_LLM_MODEL')
        )
