"""
Plot Generator Module
=====================
Generates plot structures and story outlines.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import random
from typing import List, Dict, Optional
from ..core.plot import Plot, PlotPoint

class PlotGenerator:
    """Generates plot structures and story outlines"""
    
    def __init__(self):
        # Plot templates for different genres
        self.plot_templates = {
            "mystery": {
                "hook": "A mysterious event disrupts the status quo",
                "setup": "Detective/investigator takes on the case",
                "investigation": "Clues are gathered, suspects emerge",
                "twist": "Unexpected revelation changes everything",
                "climax": "Confrontation with the truth",
                "resolution": "Mystery solved, loose ends tied"
            },
            "fantasy": {
                "hook": "An ancient prophecy begins to unfold",
                "setup": "Hero discovers their destiny",
                "journey": "Quest through magical lands",
                "trials": "Tests of courage, wisdom, and strength",
                "climax": "Final battle between good and evil",
                "resolution": "New era of peace begins"
            },
            "romance": {
                "hook": "Unexpected encounter between opposites",
                "setup": "Characters are drawn together despite differences",
                "development": "Feelings deepen, obstacles arise",
                "crisis": "Misunderstanding or external force separates them",
                "climax": "Grand gesture or realization of love",
                "resolution": "Reunion and commitment"
            },
            "adventure": {
                "hook": "Discovery of treasure map or ancient artifact",
                "setup": "Team assembles for the expedition",
                "journey": "Perilous journey through dangerous terrain",
                "obstacles": "Traps, rivals, and natural disasters",
                "climax": "Reaching the goal against all odds",
                "resolution": "Return home with treasure and wisdom"
            },
            "sci_fi": {
                "hook": "Discovery of alien technology or signal",
                "setup": "Scientists/military respond to the discovery",
                "exploration": "Journey into the unknown",
                "conflict": "First contact or technological threat",
                "climax": "Battle for survival or understanding",
                "resolution": "New relationship with the unknown"
            }
        }
        
        # Twist ideas
        self.twist_ideas = [
            "The mentor is revealed as the true villain",
            "The protagonist's memories are false",
            "The enemy is actually trying to help",
            "Everything was a simulation",
            "The sidekick was the mastermind all along",
            "The prophecy was misinterpreted",
            "The villain is a future version of the hero",
            "The quest object was inside the hero all along"
        ]
        
        # Subplot ideas
        self.subplot_ideas = [
            {"type": "friendship", "description": "Two characters develop an unlikely bond"},
            {"type": "betrayal", "description": "A trusted ally reveals their true colors"},
            {"type": "romance", "description": "Love blossoms amidst the chaos"},
            {"type": "rivalry", "description": "Friendly competition turns serious"},
            {"type": "redemption", "description": "A fallen character seeks forgiveness"},
            {"type": "discovery", "description": "Hidden talents or truths surface"}
        ]
    
    def generate_plot(self, genre: str, complexity: int = 3) -> Dict:
        """
        Generate a complete plot for a specific genre.
        
        Args:
            genre: Story genre
            complexity: Plot complexity level
            
        Returns:
            Dictionary containing the generated plot
        """
        template = self.plot_templates.get(genre, self.plot_templates["adventure"])
        
        plot = {
            "genre": genre,
            "main_plot": self._create_main_plot(template),
            "subplots": self._create_subplots(min(complexity, 4)),
            "twists": self._generate_twists(min(2, complexity)),
            "pacing": self._determine_pacing(genre),
            "estimated_length": self._estimate_length(genre, complexity)
        }
        
        return plot
    
    def _create_main_plot(self, template: Dict) -> List[Dict]:
        """Create main plot from template"""
        main_plot = []
        
        for stage, description in template.items():
            plot_point = {
                "stage": stage,
                "description": description,
                "key_events": [],
                "characters_involved": [],
                "emotional_tone": self._get_stage_tone(stage)
            }
            main_plot.append(plot_point)
        
        return main_plot
    
    def _get_stage_tone(self, stage: str) -> str:
        """Determine emotional tone for each plot stage"""
        tone_map = {
            "hook": "intriguing",
            "setup": "building",
            "investigation": "curious",
            "journey": "adventurous",
            "development": "developing",
            "trials": "tense",
            "obstacles": "challenging",
            "crisis": "emotional",
            "twist": "shocking",
            "climax": "intense",
            "resolution": "satisfying"
        }
        return tone_map.get(stage, "neutral")
    
    def _create_subplots(self, num_subplots: int) -> List[Dict]:
        """Create subplots for the story"""
        subplots = random.sample(self.subplot_ideas, 
                                min(num_subplots, len(self.subplot_ideas)))
        
        for subplot in subplots:
            subplot["status"] = "active"
            subplot["resolution_stage"] = random.choice(["midpoint", "climax", "resolution"])
        
        return subplots
    
    def _generate_twists(self, num_twists: int) -> List[str]:
        """Generate plot twists"""
        return random.sample(self.twist_ideas, min(num_twists, len(self.twist_ideas)))
    
    def _determine_pacing(self, genre: str) -> Dict:
        """Determine story pacing based on genre"""
        pacing_profiles = {
            "mystery": {"opening": "moderate", "middle": "building", "climax": "intense"},
            "fantasy": {"opening": "slow", "middle": "moderate", "climax": "epic"},
            "romance": {"opening": "gentle", "middle": "emotional", "climax": "passionate"},
            "adventure": {"opening": "fast", "middle": "action-packed", "climax": "thrilling"},
            "sci_fi": {"opening": "atmospheric", "middle": "suspenseful", "climax": "explosive"}
        }
        return pacing_profiles.get(genre, {"opening": "moderate", "middle": "moderate", "climax": "intense"})
    
    def _estimate_length(self, genre: str, complexity: int) -> Dict:
        """Estimate story length based on genre and complexity"""
        base_chapters = {
            "mystery": 20,
            "fantasy": 30,
            "romance": 18,
            "adventure": 22,
            "sci_fi": 25
        }
        
        chapters = base_chapters.get(genre, 20) + (complexity * 3)
        words_per_chapter = 2000 + (complexity * 500)
        
        return {
            "estimated_chapters": chapters,
            "estimated_words": chapters * words_per_chapter,
            "estimated_pages": (chapters * words_per_chapter) // 250
        }
    
    def suggest_twist(self, current_plot: List[Dict]) -> str:
        """Suggest a plot twist based on current plot progression"""
        # Simple logic - return random twist
        return random.choice(self.twist_ideas)
    
    def __str__(self) -> str:
        return f"PlotGenerator(genres={len(self.plot_templates)}, twists={len(self.twist_ideas)})"
