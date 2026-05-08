"""
EPUB exporter for story-toolkit.

Converts stories to EPUB format (eBooks for Amazon, Kobo, Apple Books, etc.)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import Dict, Any, List
from datetime import datetime

from .base import BaseExporter, ExportConfig


class EPUBExporter(BaseExporter):
    """Export story as EPUB eBook"""
    
    def __init__(self, config: ExportConfig = None):
        super().__init__(config)
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if required libraries are installed"""
        try:
            import ebooklib
            from ebooklib import epub
            self.ebooklib = ebooklib
            self.epub = epub
        except ImportError:
            raise ImportError(
                "EPUB export requires 'ebooklib'. "
                "Install with: pip install ebooklib"
            )
    
    def export(self, story_data: Dict[str, Any], output_path: str) -> str:
        """Export story to EPUB format"""
        from ebooklib import epub
        
        # Create EPUB book
        book = epub.EpubBook()
        
        # Set metadata
        book.set_identifier(f"story_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        book.set_title(self._get_title(story_data))
        book.set_language(self.config.language)
        book.add_author(self._get_author(story_data))
        
        # Add cover (if provided)
        if self.config.cover_image and os.path.exists(self.config.cover_image):
            with open(self.config.cover_image, 'rb') as f:
                book.set_cover("cover.jpg", f.read())
        
        # Get chapters with content
        chapters = self._get_chapters(story_data)
        epub_chapters = []
        
        for chapter in chapters:
            # Get content - try different keys
            content = chapter.get('content', '')
            if not content:
                content = chapter.get('description', '')
            if not content:
                content = f"This is chapter {chapter['number']}. No content provided."
            
            # Clean content - remove HTML if present or wrap in paragraphs
            if '<' in content and '>' in content:
                # Content already has HTML tags
                final_content = content
            else:
                # Wrap plain text in paragraphs
                paragraphs = content.split('\n\n')
                html_para = ''
                for para in paragraphs:
                    if para.strip():
                        clean_para = para.strip().replace('\n', ' ')
                        html_para += f'<p>{clean_para}</p>'
                final_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{chapter['title']}</title>
    <style>
        body {{ font-family: Georgia, serif; line-height: 1.6; margin: 2em; }}
        h1 {{ font-size: 1.5em; margin-bottom: 1em; }}
        p {{ margin-bottom: 1em; text-align: justify; }}
    </style>
</head>
<body>
    <h1>{chapter['title']}</h1>
    {html_para}
</body>
</html>
"""
            
            epub_chapter = self.epub.EpubHtml(
                title=chapter['title'],
                file_name=f'chap_{chapter["number"]:02d}.xhtml',
                lang=self.config.language
            )
            epub_chapter.content = final_content
            epub_chapters.append(epub_chapter)
            book.add_item(epub_chapter)
        
        # Define spine
        book.spine = ['nav'] + epub_chapters
        
        # Add navigation
        book.add_item(self.epub.EpubNcx())
        book.add_item(self.epub.EpubNav())
        
        # Write to file
        self.epub.write_epub(output_path, book, {})
        
        return output_path
    
    def validate(self, story_data: Dict[str, Any]) -> bool:
        """Validate story data for EPUB export"""
        required_fields = ["metadata", "plot"]
        for field in required_fields:
            if field not in story_data:
                return False
        return True
    
    def _get_chapters(self, story_data: Dict[str, Any]) -> List[Dict]:
        """Extract chapters from story data"""
        chapters = []
        plot = story_data.get("plot", {})
        main_plot = plot.get("main_plot", [])
        
        for i, stage in enumerate(main_plot, 1):
            # Get title
            title = stage.get("stage") or stage.get("name") or f"Chapter {i}"
            
            # Get content - priority: content > description
            content = stage.get("content", "")
            if not content:
                content = stage.get("description", "")
            
            chapters.append({
                "number": i,
                "title": title,
                "content": content
            })
        
        return chapters
