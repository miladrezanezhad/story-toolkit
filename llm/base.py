# story_toolkit/llm/base.py
"""Base classes and interfaces for LLM backends"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
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
    """Configuration settings for LLM backend"""
    provider: LLMProvider
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: int = 60
    retry_count: int = 3
    
    # For local backend
    local_model_path: Optional[str] = None
    
    # Caching settings
    enable_cache: bool = True
    cache_ttl: int = 3600  # seconds


class BaseLLMBackend(ABC):
    """Abstract base class for all LLM backends"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self._cache: Dict[str, tuple] = {} if config.enable_cache else None
        self._setup()
    
    @abstractmethod
    def _setup(self):
        """Initialize backend - must be implemented by child classes"""
        pass
    
    def _get_cached(self, key: str) -> Optional[str]:
        """Get cached response if available"""
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
        """Generate advanced dialogue between two characters"""
        pass
    
    def enhance_description(self, text: str, style: str = "vivid") -> str:
        """Enhance descriptive text (default implementation)"""
        prompt = f"Rewrite this text in a more {style} style without changing its meaning:\n\n{text}"
        return self.generate(prompt, max_tokens=200)
    
    def suggest_plot_twist(self, genre: str, current_plot: str, complexity: int = 3) -> str:
        """Suggest plot twists (default implementation)"""
        prompt = f"""Genre: {genre}
Current plot summary: {current_plot}
Complexity level (1-5): {complexity}

Suggest {complexity} creative but logical plot twists:"""
        return self.generate(prompt, max_tokens=400)