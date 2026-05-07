"""
Plot Module
===========
Plot management and development system.
Handles plot structure, plot points, and narrative progression.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

@dataclass
class PlotPoint:
    """A single plot point or event in the story"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    chapter: int = 0
    type: str = "event"  # event, twist, revelation, conflict
    importance: int = 1  # 1-10 scale
    characters_involved: List[str] = field(default_factory=list)
    leads_to: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class Plot:
    """
    Plot management class for story development.
    Handles plot structure, progression, and coherence.
    """
    
    def __init__(self):
        self.structure: Dict = {
            "beginning": {"hook": "", "setup": "", "inciting_incident": ""},
            "middle": {"rising_action": [], "midpoint": "", "complications": []},
            "end": {"climax": "", "falling_action": [], "resolution": ""}
        }
        self.plot_points: List[PlotPoint] = []
        self.subplots: List[Dict] = []
        self.plot_arcs: Dict = {}
        self.current_act: int = 1
        
    def add_plot_point(self, title: str, description: str, 
                       chapter: int = 0, importance: int = 5) -> PlotPoint:
        """
        Add a new plot point to the story.
        
        Args:
            title: Title of the plot point
            description: Detailed description
            chapter: Chapter number where it occurs
            importance: Importance level (1-10)
            
        Returns:
            Created PlotPoint object
        """
        point = PlotPoint(
            title=title,
            description=description,
            chapter=chapter,
            importance=importance
        )
        self.plot_points.append(point)
        return point
    
    def add_plot_point_to_structure(self, part: str, description: str) -> None:
        """Add a plot point to the story structure"""
        if part in self.structure:
            if isinstance(self.structure[part], dict):
                for key in self.structure[part]:
                    if not self.structure[part][key]:
                        self.structure[part][key] = description
                        break
            elif isinstance(self.structure[part], list):
                self.structure[part].append(description)
    
    def add_subplot(self, title: str, description: str, 
                   connected_characters: List[str] = None) -> Dict:
        """Add a subplot to the story"""
        subplot = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "description": description,
            "characters": connected_characters or [],
            "status": "active",
            "resolution": None
        }
        self.subplots.append(subplot)
        return subplot
    
    def connect_plot_points(self, point1_id: str, point2_id: str) -> None:
        """Connect two plot points to establish causality"""
        for point in self.plot_points:
            if point.id == point1_id:
                if point2_id not in point.leads_to:
                    point.leads_to.append(point2_id)
                break
    
    def get_plot_summary(self) -> Dict:
        """Get a summary of the entire plot"""
        return {
            "total_points": len(self.plot_points),
            "subplots": len(self.subplots),
            "structure_completion": self._calculate_completion(),
            "current_act": self.current_act,
            "key_points": [p for p in self.plot_points if p.importance >= 8]
        }
    
    def _calculate_completion(self) -> float:
        """Calculate plot completion percentage"""
        filled_elements = 0
        total_elements = 0
        
        for key, value in self.structure.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    total_elements += 1
                    if sub_value:
                        filled_elements += 1
            elif isinstance(value, list):
                total_elements += 1
                if value:
                    filled_elements += 1
        
        return (filled_elements / total_elements * 100) if total_elements > 0 else 0
    
    def validate_plot(self) -> List[str]:
        """Validate plot structure and identify issues"""
        issues = []
        
        # Check structure completeness
        if not self.structure["beginning"]["hook"]:
            issues.append("Missing opening hook")
        if not self.structure["end"]["climax"]:
            issues.append("Missing climax")
        if not self.structure["end"]["resolution"]:
            issues.append("Missing resolution")
        
        # Check plot points
        if len(self.plot_points) < 5:
            issues.append("Too few plot points (minimum 5 recommended)")
        
        return issues
    
    def get_plot_timeline(self) -> List[Dict]:
        """Get chronological timeline of plot points"""
        sorted_points = sorted(self.plot_points, key=lambda x: x.chapter)
        return [
            {
                "chapter": p.chapter,
                "title": p.title,
                "description": p.description,
                "importance": p.importance
            }
            for p in sorted_points
        ]
    
    def __str__(self) -> str:
        return f"Plot(points={len(self.plot_points)}, subplots={len(self.subplots)})"
    
    def __repr__(self) -> str:
        return self.__str__()
