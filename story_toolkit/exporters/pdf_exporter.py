"""
PDF exporter for story-toolkit.

Converts stories to PDF format (Print, Manuscript, and eBook styles)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base import BaseExporter, ExportConfig, PDFStyle


class PDFExporter(BaseExporter):
    """Export story as PDF document with multiple styles"""
    
    def __init__(self, config: ExportConfig = None):
        super().__init__(config)
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if required libraries are installed"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
            self.reportlab = True
        except ImportError:
            raise ImportError(
                "PDF export requires 'reportlab'. Install with: pip install reportlab"
            )
    
    def export(self, story_data: Dict[str, Any], output_path: str) -> str:
        """Export story to PDF format"""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
        
        # Create document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Define styles
        if self.config.pdf_style == PDFStyle.MANUSCRIPT:
            title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20, alignment=TA_CENTER, spaceAfter=20, fontName='Courier-Bold')
            heading_style = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=14, alignment=TA_LEFT, spaceAfter=12, fontName='Courier-Bold')
            body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=12, alignment=TA_LEFT, spaceAfter=8, fontName='Courier')
        elif self.config.pdf_style == PDFStyle.EBOOK:
            title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=24, alignment=TA_CENTER, spaceAfter=20, fontName='Helvetica-Bold')
            heading_style = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=16, alignment=TA_LEFT, spaceAfter=12, fontName='Helvetica-Bold')
            body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=12, alignment=TA_JUSTIFY, spaceAfter=8, fontName='Helvetica')
        else:  # PRINT
            title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20, alignment=TA_CENTER, spaceAfter=20, fontName='Times-Bold')
            heading_style = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=14, alignment=TA_LEFT, spaceAfter=12, fontName='Times-Bold')
            body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, alignment=TA_JUSTIFY, spaceAfter=8, fontName='Times-Roman')
        
        # Build PDF content
        pdf_elements = []
        
        # Title page
        pdf_elements.append(Paragraph(self._get_title(story_data), title_style))
        pdf_elements.append(Spacer(1, 12))
        pdf_elements.append(Paragraph(f"by {self._get_author(story_data)}", heading_style))
        pdf_elements.append(Spacer(1, 24))
        pdf_elements.append(Paragraph(datetime.now().strftime("%B %d, %Y"), body_style))
        pdf_elements.append(PageBreak())
        
        # Chapters
        chapters = self._get_chapters(story_data)
        for chapter in chapters:
            pdf_elements.append(Paragraph(f"Chapter {chapter['number']}: {chapter['title']}", heading_style))
            pdf_elements.append(Spacer(1, 12))
            
            content = chapter.get('content', '')
            if content:
                # Split into paragraphs
                for para in content.split('\n\n'):
                    if para.strip():
                        clean_para = para.strip().replace('\n', ' ')
                        pdf_elements.append(Paragraph(clean_para, body_style))
                        pdf_elements.append(Spacer(1, 8))
            else:
                pdf_elements.append(Paragraph("No content available.", body_style))
            
            pdf_elements.append(Spacer(1, 20))
            pdf_elements.append(PageBreak())
        
        # Build PDF
        doc.build(pdf_elements)
        return output_path
    
    def validate(self, story_data: Dict[str, Any]) -> bool:
        """Validate story data for PDF export"""
        return "metadata" in story_data and "plot" in story_data
    
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
    
    def export_manuscript(self, story_data: Dict[str, Any], output_path: str) -> str:
        """Export as manuscript format"""
        old_style = self.config.pdf_style
        self.config.pdf_style = PDFStyle.MANUSCRIPT
        result = self.export(story_data, output_path)
        self.config.pdf_style = old_style
        return result
    
    def export_ebook(self, story_data: Dict[str, Any], output_path: str) -> str:
        """Export as eBook format"""
        old_style = self.config.pdf_style
        self.config.pdf_style = PDFStyle.EBOOK
        result = self.export(story_data, output_path)
        self.config.pdf_style = old_style
        return result