"""
Tests for v2.1.0 - SQLite Memory

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
import uuid
from story_toolkit.memory import MemoryManager
from story_toolkit.memory.models import StoryModel, EventModel, CharacterModel, ArcStage
from story_toolkit import StoryToolkit


def test_memory_manager():
    print("\n🗄️ Testing MemoryManager (v2.1)...")
    
    manager = MemoryManager("test_memory.db")
    
    story_id = manager.create_story(
        name="Test Story",
        genre="fantasy",
        theme="courage",
        description="A test story"
    )
    
    assert story_id is not None
    assert len(story_id) > 0
    
    manager.add_event(story_id, 1, "Hero begins journey", "plot", 8)
    events = manager.get_timeline(story_id)
    
    assert len(events) == 1
    
    manager.delete_story(story_id)
    manager.close()
    
    # Cleanup
    if os.path.exists("test_memory.db"):
        os.remove("test_memory.db")
    
    print("   ✅ MemoryManager tests passed")
    return True


def test_memory_integration():
    print("\n🔗 Testing Memory Integration with Toolkit (v2.1)...")
    
    toolkit = StoryToolkit(memory_backend="sqlite", db_path="test_integration.db")
    
    story = toolkit.create_story(
        genre="fantasy",
        theme="courage",
        name="Integration Test",
        save_to_memory=True
    )
    
    hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
    toolkit.add_event(1, "Kai finds the map", "plot", 9)
    
    timeline = toolkit.get_timeline()
    characters = toolkit.list_stored_stories()
    
    assert len(timeline) == 1
    assert len(characters) >= 1
    
    toolkit.close_memory()
    
    # Cleanup
    if os.path.exists("test_integration.db"):
        os.remove("test_integration.db")
    
    print("   ✅ Memory integration tests passed")
    return True


def run_all():
    print("\n" + "="*60)
    print("🧪 V2.1.0 - MEMORY TESTS")
    print("="*60)
    
    results = []
    results.append(("MemoryManager", test_memory_manager()))
    results.append(("Memory Integration", test_memory_integration()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2.1 Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    run_all()