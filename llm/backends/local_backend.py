# story_toolkit/llm/backends/local_backend.py
"""Local backend - Support for Ollama and llama.cpp"""

from typing import List
from ..base import BaseLLMBackend

class LocalLLMBackend(BaseLLMBackend):
    """Local backend for running models on personal CPU/GPU"""
    
    def _setup(self):
        self.backend_type = None
        self.client = None
        
        # Try Ollama first
        try:
            import ollama
            self.ollama = ollama
            self.backend_type = "ollama"
            return
        except ImportError:
            pass
        
        # Try llama-cpp-python
        try:
            from llama_cpp import Llama
            if self.config.local_model_path:
                self.client = Llama(
                    model_path=self.config.local_model_path,
                    n_ctx=2048,
                    n_threads=4
                )
                self.backend_type = "llama.cpp"
            return
        except ImportError:
            pass
        
        if not self.backend_type:
            print("⚠️ No local LLM library found. Install with:")
            print("   - Ollama: pip install ollama")
            print("   - llama.cpp: pip install llama-cpp-python")
            print("   - Or use Mock backend for testing")
            self.backend_type = "none"
    
    def _call_local(self, prompt: str, **kwargs) -> str:
        """Call local model"""
        
        if self.backend_type == "ollama":
            try:
                response = self.ollama.generate(
                    model=self.config.model,
                    prompt=prompt,
                    options={
                        'temperature': kwargs.get('temperature', self.config.temperature),
                        'num_predict': kwargs.get('max_tokens', self.config.max_tokens)
                    }
                )
                return response['response']
            except Exception as e:
                return f"[Ollama Error: {str(e)}]"
        
        elif self.backend_type == "llama.cpp":
            try:
                response = self.client(
                    prompt,
                    max_tokens=kwargs.get('max_tokens', self.config.max_tokens),
                    temperature=kwargs.get('temperature', self.config.temperature),
                    echo=False
                )
                return response['choices'][0]['text']
            except Exception as e:
                return f"[llama.cpp Error: {str(e)}]"
        
        return "[Local LLM not configured. Install ollama or llama-cpp-python]"
    
    def generate(self, prompt: str, **kwargs) -> str:
        return self._call_local(prompt, **kwargs)
    
    def generate_dialogue(
        self, 
        speaker: str, 
        listener: str, 
        context: str,
        style: str = "natural",
        num_lines: int = 5,
        **kwargs
    ) -> List[str]:
        """Generate dialogue using local model"""
        
        prompt = f"""Generate a {style} dialogue between {speaker} and {listener} in {context} context.
Write exactly {num_lines} lines in format "speaker: text".
Make it natural and engaging.

Dialogue:"""
        
        response = self._call_local(prompt, **kwargs)
        
        lines = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and ':' in line:
                lines.append(line)
            elif line and lines:
                lines[-1] = lines[-1] + " " + line
        
        # Fallback to mock dialogue if response invalid
        if not lines:
            from .mock_backend import MockLLMBackend
            mock_config = self.config
            mock = MockLLMBackend(mock_config)
            return mock.generate_dialogue(speaker, listener, context, style, num_lines)
        
        return lines[:num_lines]
    
    def enhance_description(self, text: str, style: str = "vivid") -> str:
        prompt = f"Rewrite this text in {style} style: {text}"
        return self._call_local(prompt, max_tokens=200)
    
    def suggest_plot_twist(self, genre: str, current_plot: str, complexity: int = 3) -> str:
        prompt = f"Suggest {complexity} plot twists for a {genre} story: {current_plot}"
        return self._call_local(prompt, max_tokens=400)