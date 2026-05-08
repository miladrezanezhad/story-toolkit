"""
Tests for v2.2.2 - CLI Tool (Simplified)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
import json
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit import StoryToolkit
from story_toolkit.cli.commands.story import cmd_new, cmd_list_stories
from story_toolkit.cli.commands.template import cmd_list_templates, cmd_use_template


class Args:
    """Simple args class for testing"""
    pass


def test_story_new():
    """Test story new command directly"""
    print("\n🚀 Testing story new...")
    
    args = Args()
    args.genre = "fantasy"
    args.theme = "courage"
    args.complexity = 3
    args.output = None
    
    result = cmd_new(args)
    assert result is not None
    
    print("   ✅ story new works")
    return True


def test_story_new_with_complexity():
    """Test story new with complexity"""
    print("\n📊 Testing story new with complexity...")
    
    args = Args()
    args.genre = "sci_fi"
    args.theme = "survival"
    args.complexity = 5
    args.output = None
    
    result = cmd_new(args)
    assert result is not None
    
    print("   ✅ story new with complexity works")
    return True


def test_story_new_all_genres():
    """Test story new with all genres"""
    print("\n🎭 Testing story new with all genres...")
    
    genres = ["fantasy", "mystery", "romance", "adventure", "sci_fi"]
    
    for genre in genres:
        args = Args()
        args.genre = genre
        args.theme = "test"
        args.complexity = 3
        args.output = None
        
        result = cmd_new(args)
        assert result is not None
        print(f"      ✅ {genre}")
    
    print("   ✅ All genres work")
    return True


def test_template_list():
    """Test template list command"""
    print("\n📋 Testing template list...")
    
    # Just check it doesn't crash
    args = Args()
    cmd_list_templates(args)
    
    print("   ✅ template list works")
    return True


def test_template_use_hero_journey():
    """Test template use hero_journey"""
    print("\n🏰 Testing template use hero_journey...")
    
    args = Args()
    args.template = "hero_journey"
    args.genre = None
    args.theme = "adventure"
    args.output = None
    
    result = cmd_use_template(args)
    assert result is not None
    
    print("   ✅ hero_journey template works")
    return True


def test_template_use_three_act():
    """Test template use three_act"""
    print("\n🎬 Testing template use three_act...")
    
    args = Args()
    args.template = "three_act"
    args.genre = None
    args.theme = "revenge"
    args.output = None
    
    result = cmd_use_template(args)
    assert result is not None
    
    print("   ✅ three_act template works")
    return True


def test_template_use_mystery_clues():
    """Test template use mystery_clues"""
    print("\n🕵️ Testing template use mystery_clues...")
    
    args = Args()
    args.template = "mystery_clues"
    args.genre = None
    args.theme = "adventure"
    args.output = None
    
    result = cmd_use_template(args)
    assert result is not None
    
    print("   ✅ mystery_clues template works")
    return True


def test_template_use_romance_beat():
    """Test template use romance_beat"""
    print("\n💕 Testing template use romance_beat...")
    
    args = Args()
    args.template = "romance_beat"
    args.genre = None
    args.theme = "adventure"
    args.output = None
    
    result = cmd_use_template(args)
    assert result is not None
    
    print("   ✅ romance_beat template works")
    return True


def test_template_use_horror_cycle():
    """Test template use horror_cycle"""
    print("\n👻 Testing template use horror_cycle...")
    
    args = Args()
    args.template = "horror_cycle"
    args.genre = None
    args.theme = "adventure"
    args.output = None
    
    result = cmd_use_template(args)
    assert result is not None
    
    print("   ✅ horror_cycle template works")
    return True


def test_output_to_file():
    """Test saving output to file"""
    print("\n💾 Testing output to file...")
    
    # Clean up
    if os.path.exists("test_story.json"):
        os.remove("test_story.json")
    
    args = Args()
    args.genre = "fantasy"
    args.theme = "courage"
    args.complexity = 3
    args.output = "test_story.json"
    
    result = cmd_new(args)
    assert result is not None
    assert os.path.exists("test_story.json")
    
    # Verify content
    with open("test_story.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["metadata"]["genre"] == "fantasy"
    
    os.remove("test_story.json")
    
    print("   ✅ Output to file works")
    return True


def test_template_use_with_custom_genre():
    """Test template use with custom genre"""
    print("\n🎨 Testing template use with custom genre...")
    
    args = Args()
    args.template = "hero_journey"
    args.genre = "cyberpunk"
    args.theme = "survival"
    args.output = None
    
    result = cmd_use_template(args)
    assert result is not None
    assert result["metadata"]["genre"] == "cyberpunk"
    
    print("   ✅ Custom genre works")
    return True


def run_all():
    """Run all CLI tests"""
    print("\n" + "="*60)
    print("🧪 V2.2.2 - CLI TOOL TESTS (Direct)")
    print("="*60)
    
    results = []
    results.append(("story new", test_story_new()))
    results.append(("story new with complexity", test_story_new_with_complexity()))
    results.append(("story new all genres", test_story_new_all_genres()))
    results.append(("output to file", test_output_to_file()))
    results.append(("template list", test_template_list()))
    results.append(("template use hero_journey", test_template_use_hero_journey()))
    results.append(("template use three_act", test_template_use_three_act()))
    results.append(("template use mystery_clues", test_template_use_mystery_clues()))
    results.append(("template use romance_beat", test_template_use_romance_beat()))
    results.append(("template use horror_cycle", test_template_use_horror_cycle()))
    results.append(("template use custom genre", test_template_use_with_custom_genre()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 CLI Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    if all_passed:
        print("\n🎉 V2.2.2 - CLI TOOL - ALL TESTS PASSED!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
