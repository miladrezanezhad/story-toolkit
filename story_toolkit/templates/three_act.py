"""
Three Act Structure template.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List
from .base import BaseTemplate, TemplateStage


class ThreeActTemplate(BaseTemplate):
    """Three Act Structure - Setup, Confrontation, Resolution"""
    
    @property
    def name(self) -> str:
        return "three_act"
    
    @property
    def genre(self) -> str:
        return "general"
    
    @property
    def description(self) -> str:
        return "Standard three-act structure (Setup, Confrontation, Resolution)"
    
    def get_stages(self) -> List[TemplateStage]:
        return [
            TemplateStage(
                name="Act I: Setup",
                description="Introduction of characters, setting, and the initial situation. The inciting incident occurs.",
                chapter_range=(1, 8),
                examples=["Introduction of protagonist", "The problem is revealed"]
            ),
            TemplateStage(
                name="Act II: Confrontation",
                description="The protagonist faces obstacles, meets allies, and the stakes rise.",
                chapter_range=(8, 20),
                examples=["Training montage", "Rising action", "Midpoint twist"]
            ),
            TemplateStage(
                name="Act III: Resolution",
                description="The climax occurs, loose ends are tied, and the story concludes.",
                chapter_range=(20, 25),
                examples=["Final battle", "Climax", "Denouement"]
            )
        ]