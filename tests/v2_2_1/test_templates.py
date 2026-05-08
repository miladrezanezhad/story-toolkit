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
    
    # Get all templates
    templates = manager.list_templates()
    print(f"   ✅ {len(templates)} templates available")
    
    for t in templates:
        print(f"      - {t['name']} ({t['genre']}): {t['stage_count']} stages - {t['description'][:50]}...")
    
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
    for i, stage in enumerate(stages[:3], 1):
        print(f"      {i}. {stage.name}")
    print(f"      ... and {len(stages)-3} more stages")
    
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
    
    print(f"   ✅ three_act: {len(stages)} stages")
    for stage in stages:
        print(f"      - {stage.name}")
    
    return True


def test_mystery_clues_template():
    """Test mystery_clues template (5 stages)"""
    print("\n🕵️ Testing mystery_clues template...")
    
    manager = TemplateManager()
    template = manager.get_template("mystery_clues")
    
    assert template is not None
    assert template.get_stage_count() == 5
    
    stages = template.get_stages()
    expected_stages = ["The Crime", "The Investigation Begins", "The False Trail", 
                       "The Breakthrough", "The Resolution"]
    
    for i, expected in enumerate(expected_stages):
        assert stages[i].name == expected
    
    print(f"   ✅ mystery_clues: {len(stages)} stages")
    for stage in stages:
        print(f"      - {stage.name}")
    
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
    print(f"      First 3 beats: {stages[0].name}, {stages[1].name}, {stages[2].name}")
    print(f"      Last beat: {stages[-1].name}")
    
    return True


def test_horror_cycle_template():
    """Test horror_cycle template (6 stages)"""
    print("\n👻 Testing horror_cycle template...")
    
    manager = TemplateManager()
    template = manager.get_template("horror_cycle")
    
    assert template is not None
    assert template.get_stage_count() == 6
    
    stages = template.get_stages()
    expected_stages = ["The Calm Before", "The Inciting Incident", "The Investigation", 
                       "The Terror Rises", "The Confrontation", "The Aftermath"]
    
    for i, expected in enumerate(expected_stages):
        assert stages[i].name == expected
    
    print(f"   ✅ horror_cycle: {len(stages)} stages")
    for stage in stages:
        print(f"      - {stage.name}")
    
    return True


def test_apply_template_to_story():
    """Test applying template to existing story"""
    print("\n📖 Testing apply template to story...")
    
    toolkit = StoryToolkit()
    
    # Create story using template
    story = toolkit.use_template("hero_journey", genre="fantasy", theme="courage")
    
    assert story is not None
    assert "plot" in story
    assert "main_plot" in story["plot"]
    assert len(story["plot"]["main_plot"]) == 12
    assert story["metadata"]["template"] == "hero_journey"
    assert story["metadata"]["genre"] == "fantasy"
    
    print("   ✅ Story created with hero_journey template")
    return True


def test_list_templates_from_toolkit():
    """Test list_templates method from StoryToolkit"""
    print("\n🔍 Testing list_templates from Toolkit...")
    
    toolkit = StoryToolkit()
    templates = toolkit.list_templates()
    
    assert len(templates) == 5
    
    template_names = [t["name"] for t in templates]
    expected_names = ["hero_journey", "three_act", "mystery_clues", "romance_beat", "horror_cycle"]
    
    for name in expected_names:
        assert name in template_names
    
    print(f"   ✅ Found {len(templates)} templates: {', '.join(template_names)}")
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
    
    print(f"   ✅ hero_journey: {info['stage_count']} stages, {info['genre']}")
    
    # Test non-existent template
    try:
        toolkit.get_template_info("nonexistent")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "not found" in str(e)
        print(f"   ✅ Non-existent template correctly raises error")
    
    return True


def test_get_template_names():
    """Test get_template_names method"""
    print("\n📝 Testing get_template_names...")
    
    toolkit = StoryToolkit()
    names = toolkit.get_template_names()
    
    assert len(names) == 5
    assert "hero_journey" in names
    assert "three_act" in names
    assert "mystery_clues" in names
    assert "romance_beat" in names
    assert "horror_cycle" in names
    
    print(f"   ✅ Template names: {names}")
    return True


def test_template_to_dict():
    """Test template to_dict conversion"""
    print("\n📊 Testing template to_dict...")
    
    manager = TemplateManager()
    template = manager.get_template("three_act")
    
    data = template.to_dict()
    assert data["name"] == "three_act"
    assert data["stage_count"] == 3
    assert "stages" in data
    assert len(data["stages"]) == 3
    
    print(f"   ✅ three_act to_dict: {data['name']} - {data['stage_count']} stages")
    return True


def test_all_templates_create_stories():
    """Test creating stories from all templates"""
    print("\n🎭 Testing all templates create stories...")
    
    toolkit = StoryToolkit()
    templates = ["hero_journey", "three_act", "mystery_clues", "romance_beat", "horror_cycle"]
    
    for template_name in templates:
        story = toolkit.use_template(template_name)
        stages = story["plot"]["main_plot"]
        print(f"   ✅ {template_name}: {len(stages)} stages")
        assert len(stages) > 0
    
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
    results.append(("Apply Template to Story", test_apply_template_to_story()))
    results.append(("List Templates from Toolkit", test_list_templates_from_toolkit()))
    results.append(("Get Template Info", test_get_template_info()))
    results.append(("Get Template Names", test_get_template_names()))
    results.append(("Template to Dict", test_template_to_dict()))
    results.append(("All Templates Create Stories", test_all_templates_create_stories()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2.2.1 Template Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    if all_passed:
        print("\n🎉 V2.2.1 - PRE-BUILT STORY TEMPLATES - ALL TESTS PASSED!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)