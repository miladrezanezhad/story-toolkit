"""
Hero's Journey template (12 stages - Campbell's monomyth)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List
from .base import BaseTemplate, TemplateStage


class HeroJourneyTemplate(BaseTemplate):
    """Hero's Journey - 12 stage structure by Joseph Campbell"""
    
    @property
    def name(self) -> str:
        return "hero_journey"
    
    @property
    def genre(self) -> str:
        return "fantasy, adventure"
    
    @property
    def description(self) -> str:
        return "The classic hero's journey structure (Campbell's monomyth) with 12 stages"
    
    def get_stages(self) -> List[TemplateStage]:
        return [
            TemplateStage(
                name="The Ordinary World",
                description="The hero's normal life before the adventure begins.",
                chapter_range=(1, 2),
                examples=["Harry Potter living with the Dursleys", "Frodo in the Shire"]
            ),
            TemplateStage(
                name="The Call to Adventure",
                description="The hero receives a challenge or quest.",
                chapter_range=(2, 3),
                examples=["Harry's letters from Hogwarts", "Gandalf's visit to Frodo"]
            ),
            TemplateStage(
                name="Refusal of the Call",
                description="The hero hesitates or refuses the adventure.",
                chapter_range=(3, 4),
                examples=["Harry being locked in the cupboard", "Frodo wanting to stay"]
            ),
            TemplateStage(
                name="Meeting the Mentor",
                description="The hero meets a wise figure who guides them.",
                chapter_range=(4, 5),
                examples=["Hagrid telling Harry about magic", "Gandalf explaining the ring"]
            ),
            TemplateStage(
                name="Crossing the Threshold",
                description="The hero commits to the adventure and leaves the ordinary world.",
                chapter_range=(5, 7),
                examples=["Harry going to Diagon Alley", "Frodo leaving the Shire"]
            ),
            TemplateStage(
                name="Tests, Allies, and Enemies",
                description="The hero faces challenges, makes friends, and meets foes.",
                chapter_range=(7, 12),
                examples=["Harry making friends at Hogwarts", "The Fellowship forming"]
            ),
            TemplateStage(
                name="Approach to the Inmost Cave",
                description="The hero prepares for a major challenge.",
                chapter_range=(12, 15),
                examples=["Harry preparing for the final task", "Approaching Mordor"]
            ),
            TemplateStage(
                name="The Ordeal",
                description="The hero faces their greatest fear or challenge.",
                chapter_range=(15, 18),
                examples=["Harry facing Quirrell/Voldemort", "Frodo at Mount Doom"]
            ),
            TemplateStage(
                name="The Reward",
                description="The hero achieves the goal and gains the reward.",
                chapter_range=(18, 20),
                examples=["Harry getting the stone", "The ring is destroyed"]
            ),
            TemplateStage(
                name="The Road Back",
                description="The hero begins the journey home but faces more challenges.",
                chapter_range=(20, 22),
                examples=["Harry's journey back", "The escape from Mordor"]
            ),
            TemplateStage(
                name="The Resurrection",
                description="The hero faces a final test before returning.",
                chapter_range=(22, 24),
                examples=["Harry's final confrontation", "The final battle"]
            ),
            TemplateStage(
                name="Return with the Elixir",
                description="The hero returns home transformed, bringing something of value.",
                chapter_range=(24, 25),
                examples=["Harry returning to the Dursleys changed", "Frodo returning to the Shire"]
            )
        ]