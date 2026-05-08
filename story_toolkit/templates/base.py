"""
Base classes for story templates.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TemplateStage:
    """A single stage in a story template"""
    name: str
    description: str
    chapter_range: Optional[tuple] = None
    examples: List[str] = None


class BaseTemplate(ABC):
    """Abstract base class for all story templates"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Template name"""
        pass
    
    @property
    @abstractmethod
    def genre(self) -> str:
        """Story genre"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Template description"""
        pass
    
    @abstractmethod
    def get_stages(self) -> List[TemplateStage]:
        """Get all stages of the template"""
        pass
    
    def get_stage_count(self) -> int:
        """Get number of stages"""
        return len(self.get_stages())
    
    def get_stage_by_index(self, index: int) -> Optional[TemplateStage]:
        """Get stage by index (0-based)"""
        stages = self.get_stages()
        if 0 <= index < len(stages):
            return stages[index]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return {
            "name": self.name,
            "genre": self.genre,
            "description": self.description,
            "stage_count": self.get_stage_count(),
            "stages": [
                {
                    "name": stage.name,
                    "description": stage.description,
                    "chapter_range": stage.chapter_range,
                    "examples": stage.examples
                }
                for stage in self.get_stages()
            ]
        }
