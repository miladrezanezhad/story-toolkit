"""
HTML exporter for story-toolkit.

Converts stories to beautiful HTML web pages with multiple templates.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base import BaseExporter, ExportConfig, HTMLTemplate


class HTMLExporter(BaseExporter):
    """Export story as HTML web page with multiple templates"""
    
    def __init__(self, config: ExportConfig = None):
        super().__init__(config)
    
    def export(self, story_data: Dict[str, Any], output_path: str) -> str:
        """Export story to HTML format"""
        
        # Get story data
        title = self._get_title(story_data)
        author = self._get_author(story_data)
        chapters = self._get_chapters(story_data)
        characters = story_data.get("characters", [])
        
        # Select template
        if self.config.html_template == HTMLTemplate.MODERN:
            html_content = self._modern_template(title, author, chapters, characters)
        elif self.config.html_template == HTMLTemplate.CLASSIC:
            html_content = self._classic_template(title, author, chapters, characters)
        elif self.config.html_template == HTMLTemplate.DARK:
            html_content = self._dark_template(title, author, chapters, characters)
        else:  # MINIMAL
            html_content = self._minimal_template(title, author, chapters, characters)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def validate(self, story_data: Dict[str, Any]) -> bool:
        """Validate story data for HTML export"""
        required_fields = ["metadata", "plot"]
        for field in required_fields:
            if field not in story_data:
                return False
        return True
    
    def _render_chapters(self, chapters: List[Dict]) -> str:
        """Render chapters in HTML with proper content handling"""
        html = ""
        for chapter in chapters:
            # Get content - could be HTML or plain text
            content = chapter.get('content', '')
            
            # If content doesn't have HTML tags, wrap in paragraphs
            if content and not ('<' in content and '>' in content):
                # Split by double newlines into paragraphs
                paragraphs = content.split('\n\n')
                formatted_content = ''
                for para in paragraphs:
                    if para.strip():
                        # Replace single newlines with spaces
                        clean_para = para.strip().replace('\n', ' ')
                        formatted_content += f'<p>{clean_para}</p>\n'
            else:
                # Content already has HTML tags or is empty
                formatted_content = content if content else '<p>No content available.</p>'
            
            html += f"""
        <div class="chapter">
            <h2>Chapter {chapter['number']}: {chapter['title']}</h2>
            {formatted_content}
        </div>
"""
        return html
    
    def _render_chapters_classic(self, chapters: List[Dict]) -> str:
        """Render chapters in classic style with dropcap"""
        html = ""
        for chapter in chapters:
            content = chapter.get('content', '')
            
            if content and not ('<' in content and '>' in content):
                # Get first character for dropcap
                first_char = content[0] if content else ''
                rest_content = content[1:] if len(content) > 1 else ''
                formatted_content = f'<p><span class="dropcap">{first_char}</span>{rest_content}</p>'
            else:
                formatted_content = content if content else '<p>No content available.</p>'
            
            html += f"""
        <div class="chapter">
            <h2>Chapter {chapter['number']}</h2>
            {formatted_content}
        </div>
"""
        return html
    
    def _render_chapters_minimal(self, chapters: List[Dict]) -> str:
        """Render chapters in minimal style"""
        html = ""
        for chapter in chapters:
            content = chapter.get('content', '')
            
            if content and not ('<' in content and '>' in content):
                # Take first 300 characters for preview
                preview = content[:300] + '...' if len(content) > 300 else content
                formatted_content = f'<p>{preview}</p>'
            else:
                formatted_content = content if content else '<p>No content available.</p>'
            
            html += f"""
    <h2>Chapter {chapter['number']}: {chapter['title']}</h2>
    {formatted_content}
    <hr>
"""
        return html
    
    def _modern_template(self, title: str, author: str, chapters: List[Dict], characters: List) -> str:
        """Modern responsive HTML template"""
        chapters_html = self._render_chapters(chapters)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - by {author}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c3e50;
            background: #f5f7fa;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            border-bottom: 2px solid #e67e22;
            padding-bottom: 30px;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #e67e22;
            margin-bottom: 10px;
        }}
        
        .author {{
            font-size: 1.2em;
            color: #7f8c8d;
        }}
        
        .date {{
            font-size: 0.9em;
            color: #95a5a6;
            margin-top: 10px;
        }}
        
        .chapter {{
            margin-bottom: 40px;
        }}
        
        h2 {{
            font-size: 1.8em;
            color: #34495e;
            border-left: 4px solid #e67e22;
            padding-left: 15px;
            margin-bottom: 20px;
        }}
        
        p {{
            margin-bottom: 20px;
            text-align: justify;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #95a5a6;
            font-size: 0.8em;
        }}
        
        @media (max-width: 600px) {{
            .container {{ padding: 20px; }}
            h1 {{ font-size: 1.8em; }}
            h2 {{ font-size: 1.4em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="author">by {author}</div>
            <div class="date">{datetime.now().strftime("%B %d, %Y")}</div>
        </div>
        
        {chapters_html}
        
        <div class="footer">
            <p>Generated by Story Development Toolkit</p>
            <p>{datetime.now().strftime("%Y")}</p>
        </div>
    </div>
</body>
</html>"""
    
    def _classic_template(self, title: str, author: str, chapters: List[Dict], characters: List) -> str:
        """Classic book-style HTML template"""
        chapters_html = self._render_chapters_classic(chapters)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - by {author}</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            color: #000;
            background: #faf9f5;
            margin: 0;
            padding: 40px;
        }}
        
        .book {{
            max-width: 650px;
            margin: 0 auto;
            background: white;
            padding: 60px;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
        }}
        
        .title-page {{
            text-align: center;
            margin-bottom: 60px;
        }}
        
        h1 {{
            font-size: 2.2em;
            margin-bottom: 20px;
        }}
        
        .author {{
            font-size: 1.1em;
            margin-bottom: 40px;
        }}
        
        .chapter {{
            margin-bottom: 30px;
        }}
        
        h2 {{
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .dropcap {{
            font-size: 3.5em;
            float: left;
            line-height: 0.8;
            margin-right: 8px;
        }}
        
        p {{
            text-align: justify;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="book">
        <div class="title-page">
            <h1>{title}</h1>
            <div class="author">by {author}</div>
            <div class="date">{datetime.now().strftime("%Y")}</div>
        </div>
        
        {chapters_html}
        
        <div style="text-align: center; margin-top: 60px;">
            <p>THE END</p>
        </div>
    </div>
</body>
</html>"""
    
    def _dark_template(self, title: str, author: str, chapters: List[Dict], characters: List) -> str:
        """Dark theme HTML template for night reading"""
        chapters_html = self._render_chapters(chapters)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - by {author}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #e0e0e0;
            background: #1a1a2e;
            margin: 0;
            padding: 40px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            border-bottom: 2px solid #e94560;
            padding-bottom: 30px;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #e94560;
        }}
        
        .author {{
            color: #aaa;
        }}
        
        h2 {{
            color: #e94560;
            border-left: 4px solid #e94560;
            padding-left: 15px;
        }}
        
        p {{
            margin-bottom: 20px;
            text-align: justify;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="author">by {author}</div>
        </div>
        
        {chapters_html}
        
        <div class="footer">
            <p>Generated by Story Development Toolkit</p>
        </div>
    </div>
</body>
</html>"""
    
    def _minimal_template(self, title: str, author: str, chapters: List[Dict], characters: List) -> str:
        """Minimal clean HTML template"""
        chapters_html = self._render_chapters_minimal(chapters)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
        }}
        
        h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        h2 {{
            font-size: 1.3em;
            margin-top: 30px;
        }}
        
        hr {{
            margin: 30px 0;
        }}
        
        p {{
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p><em>by {author}</em></p>
    <hr>
    
    {chapters_html}
</body>
</html>"""
    
    def _get_chapters(self, story_data: Dict[str, Any]) -> List[Dict]:
        """Extract chapters from story data"""
        chapters = []
        plot = story_data.get("plot", {})
        main_plot = plot.get("main_plot", [])
        
        for i, stage in enumerate(main_plot, 1):
            title = stage.get("stage") or stage.get("name") or f"Chapter {i}"
            content = stage.get("content", "")
            if not content:
                content = stage.get("description", "")
            
            chapters.append({
                "number": i,
                "title": title,
                "content": content
            })
        
        return chapters