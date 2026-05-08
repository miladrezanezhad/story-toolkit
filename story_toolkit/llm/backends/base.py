"""
Base classes for LLM backend abstraction.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM service providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    MOCK = "mock"
    CUSTOM = "custom"


@dataclass
class LLMConfig:
    """Configuration for LLM backend"""
    provider: LLMProvider
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: int = 60
    retry_count: int = 3
    local_model_path: Optional[str] = None
    enable_cache: bool = True
    cache_ttl: int = 3600


class BaseLLMBackend(ABC):
    """Abstract base class for all LLM backends"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self._cache: Dict[str, tuple] = {} if config.enable_cache else None
        self._setup()
    
    @abstractmethod
    def _setup(self):
        """Initialize backend - implement in child class"""
        pass
    
    def _get_cached(self, key: str) -> Optional[str]:
        """Get cached response"""
        if not self.config.enable_cache:
            return None
        if key in self._cache:
            value, timestamp = self._cache[key]
            import time
            if time.time() - timestamp < self.config.cache_ttl:
                return value
        return None
    
    def _set_cache(self, key: str, value: str):
        """Store response in cache"""
        if self.config.enable_cache:
            import time
            self._cache[key] = (value, time.time())
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def generate_dialogue(
        self, 
        speaker: str, 
        listener: str, 
        context: str,
        style: str = "natural",
        num_lines: int = 5,
        **kwargs
    ) -> List[str]:
        """Generate dialogue between characters"""
        pass
