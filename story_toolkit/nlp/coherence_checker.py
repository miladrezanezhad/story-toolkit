"""
Coherence Checker Module
========================
Analyzes story coherence, consistency, and identifies plot holes.
Accepts both dictionary data and Story Toolkit objects.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import re
from typing import List, Dict, Tuple, Any, Union
from collections import defaultdict


class CoherenceChecker:
    """Checks story coherence and identifies narrative issues"""
    
    def __init__(self):
        self.consistency_rules = [
            "character_consistency",
            "timeline_coherence",
            "plot_continuity",
            "setting_consistency",
            "logic_validation"
        ]
        
        self.common_plot_holes = [
            "unexplained_character_motivation",
            "timeline_contradiction",
            "convenient_coincidence",
            "forgotten_character",
            "unresolved_subplot",
            "deus_ex_machina"
        ]
    
    def generate_coherence_report(self, story_data: Dict) -> Dict:
        """
        Generate a comprehensive coherence report.
        
        Args:
            story_data: Dictionary containing story elements
                        Can include Character objects, dicts, or mixed
            
        Returns:
            Coherence report dictionary
        """
        report = {
            "overall_score": 0.0,
            "character_consistency": {},
            "timeline": {},
            "plot_holes": [],
            "logic_issues": [],
            "recommendations": []
        }
        
        # Check character consistency
        if "characters" in story_data:
            characters_data = story_data["characters"]
            report["character_consistency"] = self.check_character_consistency(
                characters_data
            )
        
        # Check timeline coherence
        if "events" in story_data:
            report["timeline"] = self.check_timeline_coherence(
                story_data["events"]
            )
        
        # Check plot holes
        if "elements" in story_data:
            report["plot_holes"] = self.check_plot_holes(
                story_data["elements"]
            )
        
        # Calculate overall score
        scores = []
        
        if report["character_consistency"]:
            scores.append(report["character_consistency"].get("is_consistent", False))
        
        if report["timeline"]:
            scores.append(report["timeline"].get("is_coherent", False))
        
        plot_holes_score = len(report["plot_holes"]) == 0
        scores.append(plot_holes_score)
        
        report["overall_score"] = sum(scores) / len(scores) if scores else 0.0
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)
        
        return report
    
    def check_character_consistency(self, characters: List[Any]) -> Dict:
        """
        Check character consistency throughout the story.
        Accepts both dict objects and Character objects.
        
        Args:
            characters: List of character states (dict or Character objects)
            
        Returns:
            Consistency check results
        """
        issues = []
        suggestions = []
        
        # Convert all characters to uniform dict format
        processed = self._normalize_characters(characters)
        
        if len(processed) > 1:
            for i in range(1, len(processed)):
                if self._detect_abrupt_change(processed[i-1], processed[i]):
                    char_name = processed[i].get("name", f"Character {i}")
                    issues.append(
                        f"Abrupt character change detected for '{char_name}' at stage {i}"
                    )
                    suggestions.append(
                        "Consider adding transitional scenes for character development"
                    )
        
        return {
            "is_consistent": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _normalize_characters(self, characters: List[Any]) -> List[Dict]:
        """
        Convert mixed character formats to uniform dict format.
        Handles Character objects, dicts, and strings.
        
        Args:
            characters: List of characters in various formats
            
        Returns:
            List of normalized character dicts
        """
        normalized = []
        
        for i, char in enumerate(characters):
            if isinstance(char, dict):
                # Already a dict, ensure it has required fields
                normalized_char = {
                    "stage": char.get("stage", i),
                    "personality": char.get("personality", ""),
                    "name": char.get("name", f"Character {i}"),
                    "role": char.get("role", "unknown")
                }
                # If personality is empty, try traits
                if not normalized_char["personality"] and "traits" in char:
                    normalized_char["personality"] = ", ".join(char["traits"])
                normalized.append(normalized_char)
                
            elif hasattr(char, 'personality_traits'):
                # It's a Character object
                normalized.append({
                    "stage": i,
                    "personality": ", ".join(char.personality_traits) if char.personality_traits else "neutral",
                    "name": getattr(char, 'name', f"Character {i}"),
                    "role": getattr(char, 'role', "unknown"),
                    "traits": char.personality_traits,
                    "goals": getattr(char, 'goals', []),
                    "fears": getattr(char, 'fears', [])
                })
                
            elif hasattr(char, 'get'):
                # Quacks like a dict
                normalized.append({
                    "stage": char.get("stage", i),
                    "personality": char.get("personality", ""),
                    "name": char.get("name", f"Character {i}"),
                    "role": char.get("role", "unknown")
                })
                
            else:
                # Fallback for strings or other types
                normalized.append({
                    "stage": i,
                    "personality": str(char),
                    "name": f"Character {i}",
                    "role": "unknown"
                })
        
        return normalized
    
    def check_timeline_coherence(self, events: List[Dict]) -> Dict:
        """
        Check timeline coherence of events.
        
        Args:
            events: List of timeline events with timestamps
            
        Returns:
            Timeline coherence check results
        """
        issues = []
        
        # Convert events to uniform format
        processed_events = []
        for i, event in enumerate(events):
            if isinstance(event, dict):
                processed_events.append(event)
            elif hasattr(event, 'get'):
                processed_events.append({
                    "id": event.get("id", i),
                    "timestamp": event.get("timestamp", 0),
                    "description": event.get("description", "")
                })
            else:
                processed_events.append({
                    "id": i,
                    "timestamp": i * 100,
                    "description": str(event)
                })
        
        for i in range(1, len(processed_events)):
            prev_time = processed_events[i-1].get("timestamp", 0)
            curr_time = processed_events[i].get("timestamp", 0)
            
            if curr_time < prev_time:
                issues.append(
                    f"Timeline inconsistency between events {i-1} and {i}: "
                    f"timestamp {curr_time} comes after {prev_time}"
                )
        
        return {
            "is_coherent": len(issues) == 0,
            "issues": issues
        }
    
    def check_plot_holes(self, story_elements: List[Dict]) -> List[str]:
        """
        Identify plot holes in the story.
        
        Args:
            story_elements: List of story elements to check
            
        Returns:
            List of identified plot holes
        """
        plot_holes = []
        
        introduced_elements = set()
        resolved_elements = set()
        
        for element in story_elements:
            if isinstance(element, dict):
                element_id = element.get("id", str(element))
                if element.get("introduced"):
                    introduced_elements.add(element_id)
                if element.get("resolved"):
                    resolved_elements.add(element_id)
            elif hasattr(element, 'get'):
                element_id = element.get("id", str(element))
                if element.get("introduced"):
                    introduced_elements.add(element_id)
                if element.get("resolved"):
                    resolved_elements.add(element_id)
            else:
                # Simple object, assume introduced but not resolved
                introduced_elements.add(str(element))
        
        unresolved = introduced_elements - resolved_elements
        
        for item in unresolved:
            plot_holes.append(f"Unresolved plot element: {item}")
        
        return plot_holes
    
    def check_logic_consistency(self, statements: List[str]) -> List[str]:
        """
        Check logical consistency between statements.
        
        Args:
            statements: List of statements to check
            
        Returns:
            List of logic issues
        """
        issues = []
        
        for i, stmt1 in enumerate(statements):
            for j, stmt2 in enumerate(statements):
                if i < j:
                    if self._check_contradiction(stmt1, stmt2):
                        issues.append(
                            f"Potential contradiction: '{stmt1[:50]}...' vs '{stmt2[:50]}...'"
                        )
        
        return issues
    
    def _detect_abrupt_change(self, prev_state: Dict, current_state: Dict) -> bool:
        """
        Detect abrupt character changes between states.
        
        Args:
            prev_state: Previous character state dict
            current_state: Current character state dict
            
        Returns:
            True if abrupt change detected
        """
        prev_personality = prev_state.get("personality", "")
        curr_personality = current_state.get("personality", "")
        
        if prev_personality and curr_personality:
            prev_lower = prev_personality.lower()
            curr_lower = curr_personality.lower()
            
            # Define opposite trait pairs
            opposite_pairs = [
                ("brave", "cowardly"),
                ("kind", "cruel"),
                ("honest", "deceitful"),
                ("loyal", "treacherous"),
                ("compassionate", "ruthless"),
                ("generous", "greedy"),
                ("humble", "arrogant"),
                ("patient", "impulsive"),
                ("optimistic", "pessimistic"),
                ("trusting", "paranoid")
            ]
            
            for trait1, trait2 in opposite_pairs:
                # Check if trait1 in prev and trait2 in current
                if trait1 in prev_lower and trait2 in curr_lower:
                    return True
                # Check if trait2 in prev and trait1 in current
                if trait2 in prev_lower and trait1 in curr_lower:
                    return True
        
        return False
    
    def _check_contradiction(self, statement1: str, statement2: str) -> bool:
        """
        Simple contradiction check between two statements.
        
        Args:
            statement1: First statement
            statement2: Second statement
            
        Returns:
            True if potential contradiction found
        """
        negation_words = ["not", "never", "no", "don't", "doesn't", "won't", "can't"]
        
        words1 = set(statement1.lower().split())
        words2 = set(statement2.lower().split())
        
        has_negation1 = any(word in words1 for word in negation_words)
        has_negation2 = any(word in words2 for word in negation_words)
        
        # If one has negation and the other doesn't, check for similar content
        if has_negation1 != has_negation2:
            common_words = words1 & words2 - set(negation_words) - {"the", "a", "an", "is", "was", "are"}
            if len(common_words) > 2:
                return True
        
        return False
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """
        Generate recommendations based on report findings.
        
        Args:
            report: Coherence report dictionary
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        char_consistency = report.get("character_consistency", {})
        timeline = report.get("timeline", {})
        plot_holes = report.get("plot_holes", [])
        
        char_issues = char_consistency.get("issues", []) if isinstance(char_consistency, dict) else []
        timeline_issues = timeline.get("issues", []) if isinstance(timeline, dict) else []
        
        if char_issues:
            recommendations.append(
                "Review character development arcs for smoother transitions"
            )
            recommendations.append(
                "Add scenes showing gradual character growth or change"
            )
        
        if timeline_issues:
            recommendations.append(
                "Create a detailed timeline to ensure chronological consistency"
            )
            recommendations.append(
                "Verify all event timestamps are in correct order"
            )
        
        if plot_holes:
            recommendations.append(
                "Resolve outstanding plot elements and subplots"
            )
            recommendations.append(
                "Ensure all introduced story elements have proper closure"
            )
        
        if not recommendations:
            recommendations.append(
                "Story appears coherent - maintain this quality throughout!"
            )
        
        return recommendations
    
    def quick_check(self, story_data: Dict) -> bool:
        """
        Quick coherence check returning True/False.
        
        Args:
            story_data: Story data to check
            
        Returns:
            True if story passes basic coherence checks
        """
        report = self.generate_coherence_report(story_data)
        return report.get("overall_score", 0) >= 0.7
    
    def get_detailed_issues(self, story_data: Dict) -> Dict:
        """
        Get detailed breakdown of all issues found.
        
        Args:
            story_data: Story data to analyze
            
        Returns:
            Dictionary with categorized issues
        """
        report = self.generate_coherence_report(story_data)
        
        return {
            "critical_issues": [],
            "warnings": [],
            "suggestions": report.get("recommendations", []),
            "character_issues": report.get("character_consistency", {}).get("issues", []),
            "timeline_issues": report.get("timeline", {}).get("issues", []),
            "plot_holes": report.get("plot_holes", []),
            "overall_health": report.get("overall_score", 0)
        }
    
    def __str__(self) -> str:
        return f"CoherenceChecker(rules={len(self.consistency_rules)}, plot_hole_types={len(self.common_plot_holes)})"
    
    def __repr__(self) -> str:
        return self.__str__()
