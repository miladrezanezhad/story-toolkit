"""
Pre-built story templates for story-toolkit.

Available templates:
- hero_journey (12 stages - Campbell's monomyth)
- three_act (3 acts - standard structure)
- mystery_clues (5 stages - detective story)
- romance_beat (15 beats - Romancing the Beat)
- horror_cycle (5 stages - horror structure)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from .manager import TemplateManager
from .hero_journey import HeroJourneyTemplate
from .three_act import ThreeActTemplate
from .mystery_clues import MysteryCluesTemplate
from .romance_beat import RomanceBeatTemplate
from .horror_cycle import HorrorCycleTemplate

__all__ = [
    'TemplateManager',
    'HeroJourneyTemplate',
    'ThreeActTemplate',
    'MysteryCluesTemplate',
    'RomanceBeatTemplate',
    'HorrorCycleTemplate'
]
