"""
Base classes for exporters.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class ExportFormat(str, Enum):
    """Supported export formats"""
    EPUB = "epub"
    PDF = "pdf"
    HTML = "html"
    AUDIOBOOK = "audiobook"
    BIONIC_HTML = "bionic_html"


class PDFStyle(str, Enum):
    """PDF output styles"""
    PRINT = "print"           # Standard print book
    MANUSCRIPT = "manuscript" # For publishers
    EBOOK = "ebook"           # For screen reading


class HTMLTemplate(str, Enum):
    """HTML template styles"""
    MODERN = "modern"
    CLASSIC = "classic"
    DARK = "dark"
    MINIMAL = "minimal"


@dataclass
class ExportConfig:
    """Configuration for exporters"""
    format: ExportFormat = ExportFormat.EPUB
    title: Optional[str] = None
    author: Optional[str] = None
    cover_image: Optional[str] = None
    language: str = "en"
    
    # PDF specific
    pdf_style: PDFStyle = PDFStyle.PRINT
    page_size: str = "A4"
    
    # HTML specific
    html_template: HTMLTemplate = HTMLTemplate.MODERN
    embed: bool = False
    
    # Audio specific
    audio_voice: str = "en"
    audio_speed: float = 1.0
    audio_lang: str = "en"
    
    # Bionic specific
    bionic_strength: int = 1  # 1-3, how many letters to bold


class BaseExporter(ABC):
    """Abstract base class for all exporters"""
    
    def __init__(self, config: Optional[ExportConfig] = None):
        self.config = config or ExportConfig()
    
    @abstractmethod
    def export(self, story_data: Dict[str, Any], output_path: str) -> str:
        """
        Export story to specified format.
        
        Args:
            story_data: Story dictionary from StoryToolkit
            output_path: Path to save the exported file
            
        Returns:
            Path to the created file
        """
        pass
    
    @abstractmethod
    def validate(self, story_data: Dict[str, Any]) -> bool:
        """Validate if story data can be exported"""
        pass
    
    def _get_title(self, story_data: Dict[str, Any]) -> str:
        """Extract title from story data"""
        if self.config.title:
            return self.config.title
        return story_data.get("metadata", {}).get("title", "Untitled Story")
    
    def _get_author(self, story_data: Dict[str, Any]) -> str:
        """Extract author from story data"""
        if self.config.author:
            return self.config.author
        return story_data.get("metadata", {}).get("author", "Unknown Author")
    
    def _get_chapters(self, story_data: Dict[str, Any]) -> list:
        """Extract chapters from story data"""
        # This will be expanded based on actual story structure
        chapters = []
        
        # Get plot timeline
        plot = story_data.get("plot", {})
        main_plot = plot.get("main_plot", [])
        
        for i, stage in enumerate(main_plot, 1):
            chapters.append({
                "number": i,
                "title": stage.get("stage", f"Chapter {i}"),
                "content": stage.get("description", "")
            })
        
        return chapters