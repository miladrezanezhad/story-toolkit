"""
Romance Beats template (Romancing the Beat by Gwen Hayes)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List
from .base import BaseTemplate, TemplateStage


class RomanceBeatTemplate(BaseTemplate):
    """Romance story structure (15 beats)"""
    
    @property
    def name(self) -> str:
        return "romance_beat"
    
    @property
    def genre(self) -> str:
        return "romance"
    
    @property
    def description(self) -> str:
        return "15-beat romance structure based on 'Romancing the Beat'"
    
    def get_stages(self) -> List[TemplateStage]:
        return [
            TemplateStage(name="Setup", description="Introduce hero and heroine in their ordinary worlds."),
            TemplateStage(name="The Meet Cute", description="The hero and heroine meet for the first time."),
            TemplateStage(name="The Conflict", description="Something keeps them apart."),
            TemplateStage(name="The Bridge", description="Circumstances force them together."),
            TemplateStage(name="The Fun and Games", description="Romantic moments and chemistry develop."),
            TemplateStage(name="The Midpoint", description="Emotional or physical intimacy increases."),
            TemplateStage(name="The Crisis", description="Things fall apart and separation seems inevitable."),
            TemplateStage(name="The Dark Moment", description="The lowest point in the relationship."),
            TemplateStage(name="The Breakup", description="They separate, often due to misunderstanding."),
            TemplateStage(name="The Longing", description="They realize they can't live without each other."),
            TemplateStage(name="The Grand Gesture", description="One makes a romantic effort to win the other back."),
            TemplateStage(name="The Climax", description="Together they solve the external problem."),
            TemplateStage(name="The Declaration", description="Confession of love."),
            TemplateStage(name="The Epilogue", description="They live happily ever after."),
            TemplateStage(name="The Happy Ever After", description="The end of their journey together.")
        ]
