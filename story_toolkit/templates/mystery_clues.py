"""
Mystery/Detective template.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List
from .base import BaseTemplate, TemplateStage


class MysteryCluesTemplate(BaseTemplate):
    """Mystery/Detective story structure"""
    
    @property
    def name(self) -> str:
        return "mystery_clues"
    
    @property
    def genre(self) -> str:
        return "mystery"
    
    @property
    def description(self) -> str:
        return "Classic mystery story structure with clues and suspects"
    
    def get_stages(self) -> List[TemplateStage]:
        return [
            TemplateStage(
                name="The Crime",
                description="A crime is discovered. The detective is introduced.",
                chapter_range=(1, 2),
                examples=["Murder is discovered", "The investigation begins"]
            ),
            TemplateStage(
                name="The Investigation Begins",
                description="The detective gathers initial clues and suspects.",
                chapter_range=(2, 6),
                examples=["Interviewing witnesses", "Collecting evidence"]
            ),
            TemplateStage(
                name="The False Trail",
                description="A misleading clue points to the wrong suspect.",
                chapter_range=(6, 10),
                examples=["Red herring", "Wrong suspect identified"]
            ),
            TemplateStage(
                name="The Breakthrough",
                description="A key clue is discovered that changes everything.",
                chapter_range=(10, 15),
                examples=["Hidden evidence found", "Witness remembers something"]
            ),
            TemplateStage(
                name="The Resolution",
                description="The detective reveals the truth and the culprit is caught.",
                chapter_range=(15, 20),
                examples=["The reveal", "Confrontation with the killer"]
            )
        ]
