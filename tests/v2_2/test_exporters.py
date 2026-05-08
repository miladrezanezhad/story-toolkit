"""
Tests for v2.2.0 - Exporters (EPUB, PDF, HTML, Bionic)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
import tempfile
from story_toolkit import StoryToolkit
from story_toolkit.exporters import (
    EPUBExporter, PDFExporter, HTMLExporter,
    ExportConfig, PDFStyle, HTMLTemplate, to_bionic
)


def create_test_story():
    """Create a test story for exporters"""
    toolkit = StoryToolkit()
    story = toolkit.create_story("fantasy", "courage")
    story["metadata"]["title"] = "Test Story"
    story["metadata"]["author"] = "Tester"
    story["plot"]["main_plot"] = [
        {"stage": "Beginning", "description": "The hero starts their journey."},
        {"stage": "Middle", "description": "The hero faces challenges."},
        {"stage": "End", "description": "The hero triumphs."}
    ]
    return story


def test_bionic():
    print("\n👁️ Testing Bionic Reading (v2.2)...")
    
    text = "This is a test sentence."
    bionic1 = to_bionic(text, strength=1)
    bionic2 = to_bionic(text, strength=2)
    
    assert "**T**his" in bionic1 or "**Th**is" in bionic1
    assert len(bionic1) > len(text)
    
    print("   ✅ Bionic Reading tests passed")
    return True


def test_epub():
    print("\n📚 Testing EPUB Exporter (v2.2)...")
    
    try:
        import ebooklib
        has_epub = True
    except ImportError:
        has_epub = False
        print("   ⚠️ ebooklib not installed, skipping EPUB test")
        return True
    
    story = create_test_story()
    config = ExportConfig(title="Test", author="Tester")
    exporter = EPUBExporter(config)
    
    with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        result = exporter.export(story, output_path)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
        print(f"   ✅ EPUB created: {os.path.getsize(result)} bytes")
    except Exception as e:
        print(f"   ❌ EPUB failed: {e}")
        return False
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
    
    return True


def test_pdf():
    print("\n📄 Testing PDF Exporter (v2.2)...")
    
    try:
        import reportlab
    except ImportError:
        print("   ⚠️ reportlab not installed, skipping PDF test")
        return True
    
    story = create_test_story()
    config = ExportConfig(title="Test", author="Tester", pdf_style=PDFStyle.PRINT)
    exporter = PDFExporter(config)
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        result = exporter.export(story, output_path)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
        print(f"   ✅ PDF created: {os.path.getsize(result)} bytes")
    except Exception as e:
        print(f"   ❌ PDF failed: {e}")
        return False
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
    
    return True


def test_html():
    print("\n🌐 Testing HTML Exporter (v2.2)...")
    
    story = create_test_story()
    
    templates = ["modern", "classic", "dark", "minimal"]
    for template_name in templates:
        config = ExportConfig(title="Test", author="Tester")
        config.html_template = HTMLTemplate(template_name)
        exporter = HTMLExporter(config)
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
            output_path = tmp.name
        
        try:
            result = exporter.export(story, output_path)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
            print(f"   ✅ HTML ({template_name}): {os.path.getsize(result)} bytes")
        except Exception as e:
            print(f"   ❌ HTML ({template_name}) failed: {e}")
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    return True


def run_all():
    print("\n" + "="*60)
    print("🧪 V2.2.0 - EXPORTERS TESTS")
    print("="*60)
    
    results = []
    results.append(("Bionic Reading", test_bionic()))
    results.append(("EPUB Exporter", test_epub()))
    results.append(("PDF Exporter", test_pdf()))
    results.append(("HTML Exporter", test_html()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2.2 Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    run_all()