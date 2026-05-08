"""
Bionic Reading converter for story-toolkit.

Enhances readability by bolding first letters of words.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import re
from typing import List, Optional


class BionicText:
    """Convert text to Bionic Reading format"""
    
    def __init__(self, strength: int = 1):
        """
        Initialize Bionic converter.
        
        Args:
            strength: Number of letters to bold (1-3)
        """
        self.strength = min(max(strength, 1), 3)
    
    def convert(self, text: str) -> str:
        """
        Convert text to Bionic Reading format.
        
        Example:
            "This is normal text" -> "**Th**is **i**s **n**ormal **t**ext"
        """
        words = text.split()
        converted_words = []
        
        for word in words:
            # Handle punctuation
            match = re.match(r'^([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)([^\w]*)$', word)
            if match:
                word_core = match.group(1)
                punctuation = match.group(2)
            else:
                word_core = word
                punctuation = ""
            
            if len(word_core) <= self.strength:
                bold_part = word_core
                normal_part = ""
            else:
                bold_part = word_core[:self.strength]
                normal_part = word_core[self.strength:]
            
            converted = f"**{bold_part}**{normal_part}{punctuation}"
            converted_words.append(converted)
        
        return ' '.join(converted_words)
    
    def convert_html(self, text: str) -> str:
        """Convert to HTML with <strong> tags"""
        words = text.split()
        converted_words = []
        
        for word in words:
            match = re.match(r'^([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)([^\w]*)$', word)
            if match:
                word_core = match.group(1)
                punctuation = match.group(2)
            else:
                word_core = word
                punctuation = ""
            
            if len(word_core) <= self.strength:
                bold_part = word_core
                normal_part = ""
            else:
                bold_part = word_core[:self.strength]
                normal_part = word_core[self.strength:]
            
            converted = f"<strong>{bold_part}</strong>{normal_part}{punctuation}"
            converted_words.append(converted)
        
        return ' '.join(converted_words)


def to_bionic(text: str, strength: int = 1, as_html: bool = False) -> str:
    """
    Convert text to Bionic Reading format.
    
    Args:
        text: Input text to convert
        strength: Number of letters to bold (1-3)
        as_html: Return as HTML with <strong> tags
    
    Example:
        >>> to_bionic("This is a test")
        '**Th**is **i**s **a** **t**est'
        >>> to_bionic("This is a test", as_html=True)
        '<strong>Th</strong>is <strong>i</strong>s <strong>a</strong> <strong>t</strong>est'
    """
    converter = BionicText(strength)
    if as_html:
        return converter.convert_html(text)
    return converter.convert(text)


def process_story(story_data: dict, strength: int = 1) -> dict:
    """
    Process entire story with Bionic Reading format.
    
    Args:
        story_data: Story dictionary from StoryToolkit
        strength: Number of letters to bold (1-3)
    
    Returns:
        Story dictionary with Bionic formatted content
    """
    converter = BionicText(strength)
    
    # Process dialogue scenes
    if "dialogue_scenes" in story_data:
        for i, scene in enumerate(story_data["dialogue_scenes"]):
            if isinstance(scene, list):
                for j, line in enumerate(scene):
                    story_data["dialogue_scenes"][i][j] = converter.convert(line)
    
    # Process plot descriptions
    if "plot" in story_data and "main_plot" in story_data["plot"]:
        for stage in story_data["plot"]["main_plot"]:
            if "description" in stage:
                stage["description"] = converter.convert(stage["description"])
    
    return story_data
