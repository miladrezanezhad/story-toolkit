"""
Tests for helper functions.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import json
import tempfile
from datetime import datetime
from story_toolkit.utils.helpers import (
    save_story, load_story, export_to_markdown, format_story_stats
)
from story_toolkit.core.character import Character


def create_sample_story():
    """Create a sample story for testing"""
    story = {
        "metadata": {
            "genre": "fantasy",
            "theme": "courage",
            "complexity": 4,
            "created_at": datetime.now().isoformat()
        },
        "characters": [],
        "plot": {
            "main_plot": [
                {"stage": "Beginning", "description": "The hero starts their journey."},
                {"stage": "Middle", "description": "The hero faces challenges."},
                {"stage": "End", "description": "The hero triumphs."}
            ]
        },
        "dialogue_scenes": [
            [
                "Hero: I will defeat you!",
                "Villain: You can try!"
            ]
        ],
        "coherence_report": {
            "overall_score": 0.95,
            "recommendations": ["Good job!", "Keep going!"]
        }
    }
    
    # Add a real character
    hero = Character("Kai", 25, "protagonist")
    hero.add_trait("brave")
    story["characters"].append(hero)
    
    return story


def test_save_story():
    """Test saving story to file"""
    print("\n💾 Testing save_story...")
    
    story = create_sample_story()
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = save_story(story, tmp_path)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
        
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data["metadata"]["genre"] == "fantasy"
        
        print("   ✅ save_story works")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_save_story_with_directory():
    """Test saving story to a nested directory"""
    print("\n📁 Testing save_story with nested directory...")
    
    story = create_sample_story()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_path = os.path.join(tmpdir, "subdir", "nested", "story.json")
        result = save_story(story, nested_path)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
        
        print("   ✅ save_story with nested directory works")
    
    return True


def test_save_story_with_character_objects():
    """Test saving story with Character objects (serialization)"""
    print("\n🎭 Testing save_story with Character objects...")
    
    story = create_sample_story()
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = save_story(story, tmp_path)
        assert os.path.exists(result)
        
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
            characters = data.get("characters", [])
            assert len(characters) == 1
            assert characters[0]["name"] == "Kai"
        
        print("   ✅ Character objects serialized correctly")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_load_story():
    """Test loading story from file"""
    print("\n📖 Testing load_story...")
    
    story = create_sample_story()
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        save_story(story, tmp_path)
        loaded = load_story(tmp_path)
        
        assert loaded is not None
        assert loaded["metadata"]["genre"] == "fantasy"
        assert len(loaded["plot"]["main_plot"]) == 3
        
        print("   ✅ load_story works")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_load_story_file_not_found():
    """Test load_story with non-existent file"""
    print("\n❌ Testing load_story with missing file...")
    
    try:
        load_story("nonexistent_file_12345.json")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        print("   ✅ FileNotFoundError raised correctly")
    
    return True


def test_export_to_markdown():
    """Test exporting story to markdown"""
    print("\n📝 Testing export_to_markdown...")
    
    story = create_sample_story()
    
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = export_to_markdown(story, tmp_path)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
        
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "fantasy" in content
            assert "courage" in content
            assert "Kai" in content
            assert "Beginning" in content
        
        print("   ✅ export_to_markdown works")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_export_to_markdown_without_dialogues():
    """Test exporting story without dialogue scenes"""
    print("\n📝 Testing export_to_markdown without dialogues...")
    
    story = create_sample_story()
    story["dialogue_scenes"] = []
    
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = export_to_markdown(story, tmp_path)
        assert os.path.exists(result)
        
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Dialogues" not in content
        
        print("   ✅ export_to_markdown without dialogues works")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_export_to_markdown_without_coherence():
    """Test exporting story without coherence report"""
    print("\n📝 Testing export_to_markdown without coherence...")
    
    story = create_sample_story()
    story.pop("coherence_report", None)
    
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = export_to_markdown(story, tmp_path)
        assert os.path.exists(result)
        
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Coherence" not in content
        
        print("   ✅ export_to_markdown without coherence works")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_format_story_stats():
    """Test formatting story statistics"""
    print("\n📊 Testing format_story_stats...")
    
    story = create_sample_story()
    stats = format_story_stats(story)
    
    assert "fantasy" in stats
    assert "courage" in stats
    assert "Characters: 1" in stats
    assert "Plot Points: 3" in stats
    assert "95%" in stats
    
    print("   ✅ format_story_stats works")
    return True


def test_format_story_stats_without_coherence():
    """Test formatting stats without coherence report"""
    print("\n📊 Testing format_story_stats without coherence...")
    
    story = create_sample_story()
    story.pop("coherence_report", None)
    
    stats = format_story_stats(story)
    
    assert "fantasy" in stats
    assert "courage" in stats
    assert "Coherence Score" not in stats
    
    print("   ✅ format_story_stats without coherence works")
    return True


def test_format_story_stats_empty():
    """Test formatting stats for empty story"""
    print("\n📊 Testing format_story_stats with empty story...")
    
    empty_story = {}
    stats = format_story_stats(empty_story)
    
    assert "N/A" in stats
    
    print("   ✅ format_story_stats with empty story works")
    return True


def test_save_story_adds_timestamp():
    """Test that save_story adds timestamp to metadata"""
    print("\n🕐 Testing save_story adds timestamp...")
    
    story = create_sample_story()
    story["metadata"].pop("saved_at", None)
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = save_story(story, tmp_path)
        assert os.path.exists(result)
        
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert "saved_at" in data.get("metadata", {})
        
        print("   ✅ Timestamp added automatically")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def test_save_story_preserves_existing_data():
    """Test that save_story preserves existing story data"""
    print("\n🔒 Testing save_story preserves data...")
    
    story = create_sample_story()
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        save_story(story, tmp_path)
        
        with open(tmp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data["metadata"]["genre"] == "fantasy"
            assert data["metadata"]["theme"] == "courage"
            assert len(data["characters"]) == 1
            assert len(data["plot"]["main_plot"]) == 3
        
        print("   ✅ All data preserved")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return True


def run_all():
    """Run all helper tests"""
    print("\n" + "="*60)
    print("🧪 HELPER FUNCTIONS TESTS")
    print("="*60)
    
    results = []
    results.append(("save_story", test_save_story()))
    results.append(("save_story with nested directory", test_save_story_with_directory()))
    results.append(("save_story with Character objects", test_save_story_with_character_objects()))
    results.append(("save_story adds timestamp", test_save_story_adds_timestamp()))
    results.append(("save_story preserves data", test_save_story_preserves_existing_data()))
    results.append(("load_story", test_load_story()))
    results.append(("load_story file not found", test_load_story_file_not_found()))
    results.append(("export_to_markdown", test_export_to_markdown()))
    results.append(("export_to_markdown without dialogues", test_export_to_markdown_without_dialogues()))
    results.append(("export_to_markdown without coherence", test_export_to_markdown_without_coherence()))
    results.append(("format_story_stats", test_format_story_stats()))
    results.append(("format_story_stats without coherence", test_format_story_stats_without_coherence()))
    results.append(("format_story_stats empty", test_format_story_stats_empty()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 Helper Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)