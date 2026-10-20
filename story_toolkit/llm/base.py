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
    GEMINI = "gemini"
    OPENCODE = "opencode"
    CLOUDFLARE = "cloudflare"
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
    proxy: Optional[str] = None
    account_id: Optional[str] = None


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

    def _make_http_request(self, url: str, payload: dict, headers: dict = None) -> dict:
        """Send a JSON POST request with optional proxy support"""
        import urllib.request
        import json

        req_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Story-Toolkit/2.2.3"
        }
        if headers:
            req_headers.update(headers)

        handlers = []
        if self.config.proxy and self.config.proxy.strip():
            proxy_url = self.config.proxy.strip()
            handlers.append(urllib.request.ProxyHandler({
                'http': proxy_url,
                'https': proxy_url
            }))

        opener = urllib.request.build_opener(*handlers)
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=req_headers, method="POST")

        with opener.open(req, timeout=self.config.timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    
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
