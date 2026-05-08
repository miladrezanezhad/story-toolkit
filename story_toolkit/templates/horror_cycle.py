"""
Horror Cycle template.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List
from .base import BaseTemplate, TemplateStage


class HorrorCycleTemplate(BaseTemplate):
    """Horror story structure"""
    
    @property
    def name(self) -> str:
        return "horror_cycle"
    
    @property
    def genre(self) -> str:
        return "horror"
    
    @property
    def description(self) -> str:
        return "Classic horror structure with rising terror"
    
    def get_stages(self) -> List[TemplateStage]:
        return [
            TemplateStage(
                name="The Calm Before",
                description="Normal life. The characters are introduced.",
                chapter_range=(1, 2),
                examples=["Peaceful opening", "Character introductions"]
            ),
            TemplateStage(
                name="The Inciting Incident",
                description="Something strange or disturbing occurs.",
                chapter_range=(2, 4),
                examples=["Weird noise", "Discovery of something strange"]
            ),
            TemplateStage(
                name="The Investigation",
                description="Characters investigate but find little.",
                chapter_range=(4, 8),
                examples=["Research", "Questioning locals"]
            ),
            TemplateStage(
                name="The Terror Rises",
                description="Increasingly scary events. Deaths may occur.",
                chapter_range=(8, 15),
                examples=["Attack", "Disappearance", "Evidence of evil"]
            ),
            TemplateStage(
                name="The Confrontation",
                description="Final showdown with the evil force.",
                chapter_range=(15, 20),
                examples=["Final battle", "Sacrifice", "The evil is defeated"]
            ),
            TemplateStage(
                name="The Aftermath",
                description="Survivors try to return to normal life.",
                chapter_range=(20, 22),
                examples=["Healing", "Memorial", "Final threat hint"]
            )
        ]