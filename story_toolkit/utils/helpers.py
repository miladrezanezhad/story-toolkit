"""
Helper Functions Module
=======================
Utility functions for file operations and data formatting.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import json
import os
from typing import Dict, Any
from datetime import datetime


def save_story(story_data: Dict, filename: str) -> str:
    """
    Save story data to a JSON file.
    
    Args:
        story_data: Story data dictionary
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', 
               exist_ok=True)
    
    # Convert to serializable format
    serializable_data = _make_serializable(story_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, ensure_ascii=False, indent=2)
    
    return os.path.abspath(filename)


def load_story(filename: str) -> Dict:
    """
    Load story data from a JSON file.
    
    Args:
        filename: Input filename
        
    Returns:
        Story data dictionary
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def export_to_markdown(story_data: Dict, filename: str) -> str:
    """
    Export story to markdown format.
    
    Args:
        story_data: Story data dictionary
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    md_content = _convert_to_markdown(story_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return os.path.abspath(filename)


def format_story_stats(story_data: Dict) -> str:
    """
    Format story statistics as a readable string.
    
    Args:
        story_data: Story data dictionary
        
    Returns:
        Formatted statistics string
    """
    stats = []
    
    metadata = story_data.get("metadata", {})
    stats.append(f"Genre: {metadata.get('genre', 'N/A')}")
    stats.append(f"Theme: {metadata.get('theme', 'N/A')}")
    stats.append(f"Complexity: {metadata.get('complexity', 'N/A')}")
    
    characters = story_data.get("characters", [])
    stats.append(f"Characters: {len(characters)}")
    
    plot = story_data.get("plot", {})
    stats.append(f"Plot Points: {len(plot.get('main_plot', []))}")
    
    if "coherence_report" in story_data:
        score = story_data["coherence_report"].get("overall_score", 0)
        stats.append(f"Coherence Score: {score:.2%}")
    
    return "\n".join(stats)


def _make_serializable(obj: Any) -> Any:
    """Convert objects to JSON-serializable format"""
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _make_serializable(value) for key, value in obj.items()}
    return obj


def _convert_to_markdown(story_data: Dict) -> str:
    """Convert story data to markdown format"""
    md = []
    
    # Title
    metadata = story_data.get("metadata", {})
    title = f"{metadata.get('genre', 'Story').title()} - {metadata.get('theme', 'Theme').title()}"
    md.append(f"# {title}\n")
    
    # Metadata
    md.append("## Story Metadata\n")
    md.append(f"- **Genre**: {metadata.get('genre', 'N/A')}")
    md.append(f"- **Theme**: {metadata.get('theme', 'N/A')}")
    md.append(f"- **Complexity**: {metadata.get('complexity', 'N/A')}")
    md.append(f"- **Created**: {metadata.get('created_at', 'N/A')}\n")
    
    # Characters
    characters = story_data.get("characters", [])
    if characters:
        md.append("## Characters\n")
        for char in characters:
            name = char.get("name", "Unknown") if isinstance(char, dict) else getattr(char, "name", "Unknown")
            role = char.get("role", "N/A") if isinstance(char, dict) else getattr(char, "role", "N/A")
            md.append(f"### {name} ({role})\n")
            
            traits = char.get("traits", []) if isinstance(char, dict) else getattr(char, "personality_traits", [])
            if traits:
                md.append(f"**Traits**: {', '.join(traits)}\n")
    
    # Plot
    plot = story_data.get("plot", {})
    main_plot = plot.get("main_plot", [])
    if main_plot:
        md.append("## Plot Structure\n")
        for point in main_plot:
            stage = point.get("stage", "Unknown Stage")
            description = point.get("description", "")
            md.append(f"### {stage.replace('_', ' ').title()}\n")
            md.append(f"{description}\n")
    
    # Dialogue Scenes
    dialogues = story_data.get("dialogue_scenes", [])
    if dialogues:
        md.append("## Key Dialogues\n")
        for i, dialogue in enumerate(dialogues, 1):
            md.append(f"### Scene {i}\n")
            if isinstance(dialogue, list):
                for line in dialogue:
                    md.append(f"- {line}\n")
            md.append("")
    
    # Coherence Report
    report = story_data.get("coherence_report", {})
    if report:
        md.append("## Coherence Report\n")
        md.append(f"**Overall Score**: {report.get('overall_score', 0):.2%}\n")
        
        recommendations = report.get("recommendations", [])
        if recommendations:
            md.append("### Recommendations\n")
            for rec in recommendations:
                md.append(f"- {rec}\n")
    
    return "\n".join(md)
