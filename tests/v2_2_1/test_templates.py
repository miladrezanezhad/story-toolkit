"""
Tests for v2.2.1 - Pre-built Story Templates

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit import StoryToolkit
from story_toolkit.templates import TemplateManager


def test_template_manager():
    """Test TemplateManager - list all templates"""
    print("\n📋 Testing TemplateManager...")
    
    manager = TemplateManager()
    templates = manager.list_templates()
    
    print(f"   ✅ {len(templates)} templates available")
    for t in templates:
        print(f"      - {t['name']} ({t['genre']}): {t['stage_count']} stages")
    
    assert len(templates) == 5
    return True


def test_hero_journey_template():
    """Test hero_journey template (12 stages)"""
    print("\n🏰 Testing hero_journey template...")
    
    manager = TemplateManager()
    template = manager.get_template("hero_journey")
    
    assert template is not None
    assert template.name == "hero_journey"
    assert template.get_stage_count() == 12
    
    stages = template.get_stages()
    assert stages[0].name == "The Ordinary World"
    assert stages[-1].name == "Return with the Elixir"
    
    print(f"   ✅ hero_journey: {len(stages)} stages")
    return True


def test_three_act_template():
    """Test three_act template (3 acts)"""
    print("\n🎬 Testing three_act template...")
    
    manager = TemplateManager()
    template = manager.get_template("three_act")
    
    assert template is not None
    assert template.get_stage_count() == 3
    
    stages = template.get_stages()
    assert stages[0].name == "Act I: Setup"
    assert stages[1].name == "Act II: Confrontation"
    assert stages[2].name == "Act III: Resolution"
    
    print("   ✅ three_act template works")
    return True


def test_mystery_clues_template():
    """Test mystery_clues template (5 stages)"""
    print("\n🕵️ Testing mystery_clues template...")
    
    manager = TemplateManager()
    template = manager.get_template("mystery_clues")
    
    assert template is not None
    assert template.get_stage_count() == 5
    
    stages = template.get_stages()
    expected = ["The Crime", "The Investigation Begins", "The False Trail", 
                "The Breakthrough", "The Resolution"]
    
    for i, expected_name in enumerate(expected):
        assert stages[i].name == expected_name
    
    print("   ✅ mystery_clues template works")
    return True


def test_romance_beat_template():
    """Test romance_beat template (15 beats)"""
    print("\n💕 Testing romance_beat template...")
    
    manager = TemplateManager()
    template = manager.get_template("romance_beat")
    
    assert template is not None
    assert template.get_stage_count() == 15
    
    stages = template.get_stages()
    assert stages[0].name == "Setup"
    assert stages[-1].name == "The Happy Ever After"
    
    print(f"   ✅ romance_beat: {len(stages)} stages")
    return True


def test_horror_cycle_template():
    """Test horror_cycle template (6 stages)"""
    print("\n👻 Testing horror_cycle template...")
    
    manager = TemplateManager()
    template = manager.get_template("horror_cycle")
    
    assert template is not None
    assert template.get_stage_count() == 6
    
    stages = template.get_stages()
    expected = ["The Calm Before", "The Inciting Incident", "The Investigation",
                "The Terror Rises", "The Confrontation", "The Aftermath"]
    
    for i, expected_name in enumerate(expected):
        assert stages[i].name == expected_name
    
    print("   ✅ horror_cycle template works")
    return True


def test_apply_template():
    """Test applying template to story"""
    print("\n📖 Testing apply template to story...")
    
    toolkit = StoryToolkit()
    story = toolkit.use_template("hero_journey", genre="fantasy", theme="courage")
    
    assert story is not None
    assert "plot" in story
    assert len(story["plot"]["main_plot"]) == 12
    assert story["metadata"]["template"] == "hero_journey"
    
    print("   ✅ Template applied successfully")
    return True


def test_list_templates_from_toolkit():
    """Test list_templates method from StoryToolkit"""
    print("\n🔍 Testing list_templates from Toolkit...")
    
    toolkit = StoryToolkit()
    templates = toolkit.list_templates()
    
    assert len(templates) == 5
    template_names = [t["name"] for t in templates]
    expected = ["hero_journey", "three_act", "mystery_clues", "romance_beat", "horror_cycle"]
    
    for name in expected:
        assert name in template_names
    
    print(f"   ✅ Found {len(templates)} templates")
    return True


def test_get_template_info():
    """Test get_template_info method"""
    print("\nℹ️ Testing get_template_info...")
    
    toolkit = StoryToolkit()
    info = toolkit.get_template_info("hero_journey")
    
    assert info["name"] == "hero_journey"
    assert info["stage_count"] == 12
    assert "stages" in info
    assert len(info["stages"]) == 12
    
    print(f"   ✅ hero_journey: {info['stage_count']} stages")
    return True


def run_all():
    """Run all v2.2.1 tests"""
    print("\n" + "="*60)
    print("🧪 V2.2.1 - PRE-BUILT STORY TEMPLATES TESTS")
    print("="*60)
    
    results = []
    results.append(("Template Manager", test_template_manager()))
    results.append(("Hero Journey Template", test_hero_journey_template()))
    results.append(("Three Act Template", test_three_act_template()))
    results.append(("Mystery Clues Template", test_mystery_clues_template()))
    results.append(("Romance Beat Template", test_romance_beat_template()))
    results.append(("Horror Cycle Template", test_horror_cycle_template()))
    results.append(("Apply Template", test_apply_template()))
    results.append(("List Templates", test_list_templates_from_toolkit()))
    results.append(("Get Template Info", test_get_template_info()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2.2.1 Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    if all_passed:
        print("\n🎉 V2.2.1 - PRE-BUILT STORY TEMPLATES - ALL TESTS PASSED!")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)