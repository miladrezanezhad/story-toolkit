"""
Tests for v2.1.0 - SQLite Memory Layer

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
import tempfile
from story_toolkit import StoryToolkit
from story_toolkit.memory import MemoryManager


def test_memory_imports():
    """Test memory module imports"""
    print("\n💾 1. Testing Memory Module Imports...")
    
    from story_toolkit.memory import MemoryManager, SQLiteMemory, MemoryConfig
    from story_toolkit.memory.models import StoryModel, EventModel, CharacterModel
    
    assert MemoryManager is not None
    assert SQLiteMemory is not None
    
    print("   ✅ Memory imports passed")
    return True


def test_memory_manager_creation():
    """Test MemoryManager creation"""
    print("\n🔧 2. Testing MemoryManager Creation...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        assert manager is not None
        print(f"   ✅ MemoryManager created with db: {db_path}")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_create_story():
    """Test creating a story in memory"""
    print("\n📖 3. Testing Create Story in Memory...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Test Story",
            genre="fantasy",
            theme="courage",
            description="A test story for memory"
        )
        
        assert story_id is not None
        assert len(story_id) == 8
        
        print(f"   ✅ Story created with ID: {story_id}")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_get_story():
    """Test retrieving a story from memory"""
    print("\n📖 4. Testing Get Story from Memory...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Test Story",
            genre="fantasy",
            theme="courage",
            description="A test story"
        )
        
        story = manager.get_story(story_id)
        
        assert story is not None
        assert story.name == "Test Story"
        assert story.genre == "fantasy"
        assert story.theme == "courage"
        
        print(f"   ✅ Story retrieved: {story.name}")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_list_stories():
    """Test listing all stories"""
    print("\n📚 5. Testing List Stories...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        for i in range(3):
            manager.create_story(
                name=f"Story {i+1}",
                genre="fantasy",
                theme="courage",
                description=f"Test story {i+1}"
            )
        
        stories = manager.list_stories()
        
        assert len(stories) == 3
        print(f"   ✅ Listed {len(stories)} stories")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_delete_story():
    """Test deleting a story"""
    print("\n🗑️ 6. Testing Delete Story...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="To Delete",
            genre="fantasy",
            theme="courage",
            description="Will be deleted"
        )
        
        assert manager.get_story(story_id) is not None
        
        result = manager.delete_story(story_id)
        assert result is True
        
        assert manager.get_story(story_id) is None
        
        print("   ✅ Story deleted successfully")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_add_event():
    """Test adding events to timeline"""
    print("\n📅 7. Testing Add Event...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Event Story",
            genre="fantasy",
            theme="courage"
        )
        
        event_id = manager.add_event(
            story_id=story_id,
            chapter=1,
            description="Hero finds the map",
            event_type="plot",
            importance=9
        )
        
        assert event_id is not None
        assert event_id > 0
        
        print(f"   ✅ Event added with ID: {event_id}")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_get_timeline():
    """Test retrieving timeline events"""
    print("\n📅 8. Testing Get Timeline...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Timeline Story",
            genre="fantasy",
            theme="courage"
        )
        
        # Valid event types: plot, dialogue, character_development, conflict, revelation, resolution, general
        events = [
            (1, "Hero discovers map", "plot", 8),
            (2, "Villain attacks village", "conflict", 10),
            (3, "Hero meets mentor", "character_development", 7),
            (4, "Training begins", "general", 6),
            (5, "Final battle", "conflict", 10),
        ]
        
        for chapter, desc, etype, importance in events:
            manager.add_event(story_id, chapter, desc, etype, importance)
        
        timeline = manager.get_timeline(story_id)
        
        assert len(timeline) == 5
        assert timeline[0].description == "Hero discovers map"
        assert timeline[-1].description == "Final battle"
        
        print(f"   ✅ Timeline has {len(timeline)} events")
        for event in timeline[:3]:
            print(f"      Ch.{event.chapter}: {event.description}")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_add_character():
    """Test adding character to memory"""
    print("\n👤 9. Testing Add Character...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Character Story",
            genre="fantasy",
            theme="courage"
        )
        
        char_id = manager.add_character(
            story_id=story_id,
            name="Kai",
            role="protagonist",
            traits=["brave", "determined"]
        )
        
        assert char_id is not None
        assert len(char_id) == 8
        
        print(f"   ✅ Character added with ID: {char_id}")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_get_characters():
    """Test retrieving characters from memory"""
    print("\n👥 10. Testing Get Characters...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Characters Story",
            genre="fantasy",
            theme="courage"
        )
        
        characters = [
            ("Kai", "protagonist", ["brave", "kind"]),
            ("Shadow Lord", "antagonist", ["cunning", "ruthless"]),
            ("Master Yuki", "mentor", ["wise", "patient"]),
        ]
        
        for name, role, traits in characters:
            manager.add_character(story_id, name, role, traits)
        
        retrieved = manager.get_characters(story_id)
        
        assert len(retrieved) == 3
        assert retrieved[0].name == "Kai"
        
        print(f"   ✅ Retrieved {len(retrieved)} characters")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_search_memory():
    """Test searching memory by keyword"""
    print("\n🔍 11. Testing Search Memory...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Search Story",
            genre="fantasy",
            theme="courage"
        )
        
        manager.add_event(story_id, 1, "Hero finds the magic sword", "plot", 9)
        manager.add_event(story_id, 2, "Hero meets the dragon", "conflict", 8)
        manager.add_event(story_id, 3, "Villain steals the sword", "conflict", 10)
        
        results = manager.search(story_id, "sword")
        assert len(results) == 2
        
        results = manager.search(story_id, "dragon")
        assert len(results) == 1
        
        print("   ✅ Search works")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_check_consistency():
    """Test consistency checking"""
    print("\n✅ 12. Testing Check Consistency...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        manager = MemoryManager(db_path)
        
        story_id = manager.create_story(
            name="Consistency Story",
            genre="fantasy",
            theme="courage"
        )
        
        manager.add_event(story_id, 1, "Event 1", "plot", 8)
        manager.add_event(story_id, 2, "Event 2", "plot", 9)
        
        issues = manager.check_consistency(story_id)
        
        assert isinstance(issues, list)
        
        print("   ✅ Consistency check passed")
        manager.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_toolkit_memory_integration():
    """Test memory integration with StoryToolkit"""
    print("\n🔗 13. Testing Toolkit Memory Integration...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=db_path)
        
        story = toolkit.create_story(
            genre="fantasy",
            theme="courage",
            name="Toolkit Story",
            save_to_memory=True
        )
        
        assert toolkit._current_story_id is not None
        
        hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
        hero.add_trait("brave")
        
        toolkit.add_event(1, "Hero finds map", "plot", 9)
        
        timeline = toolkit.get_timeline()
        assert len(timeline) == 1
        
        stories = toolkit.list_stored_stories()
        assert len(stories) >= 1
        
        print("   ✅ Toolkit memory integration works")
        toolkit.close_memory()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_load_story_from_memory():
    """Test loading a story from memory"""
    print("\n📖 14. Testing Load Story from Memory...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=db_path)
        
        story = toolkit.create_story(
            genre="fantasy",
            theme="courage",
            name="Load Test Story",
            save_to_memory=True
        )
        
        story_id = toolkit._current_story_id
        
        hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
        
        toolkit.close_memory()
        
        toolkit2 = StoryToolkit(memory_backend="sqlite", db_path=db_path)
        
        loaded = toolkit2.load_story_from_memory(story_id)
        
        assert loaded is not None
        assert loaded["metadata"]["name"] == "Load Test Story"
        assert len(loaded["characters"]) == 1
        assert loaded["characters"][0].name == "Kai"
        
        print("   ✅ Story loaded successfully")
        toolkit2.close_memory()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def test_prevent_duplicate_characters():
    """Test that duplicate characters are not saved"""
    print("\n🛡️ 15. Testing Duplicate Character Prevention...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=db_path)
        
        story = toolkit.create_story(
            genre="fantasy",
            theme="courage",
            name="No Duplicates",
            save_to_memory=True
        )
        
        toolkit.add_character_to_story(story, "Kai", "protagonist")
        toolkit.add_character_to_story(story, "Kai", "protagonist")
        
        characters = toolkit._memory.get_characters(toolkit._current_story_id)
        assert len(characters) == 1
        
        print("   ✅ Duplicate prevented")
        toolkit.close_memory()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    
    return True


def run_all():
    """Run all memory tests"""
    print("\n" + "="*60)
    print("🧪 V2.1.0 - MEMORY LAYER TESTS")
    print("="*60)
    
    results = []
    results.append(("Memory Imports", test_memory_imports()))
    results.append(("MemoryManager Creation", test_memory_manager_creation()))
    results.append(("Create Story", test_create_story()))
    results.append(("Get Story", test_get_story()))
    results.append(("List Stories", test_list_stories()))
    results.append(("Delete Story", test_delete_story()))
    results.append(("Add Event", test_add_event()))
    results.append(("Get Timeline", test_get_timeline()))
    results.append(("Add Character", test_add_character()))
    results.append(("Get Characters", test_get_characters()))
    results.append(("Search Memory", test_search_memory()))
    results.append(("Check Consistency", test_check_consistency()))
    results.append(("Toolkit Integration", test_toolkit_memory_integration()))
    results.append(("Load Story", test_load_story_from_memory()))
    results.append(("Duplicate Prevention", test_prevent_duplicate_characters()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V2.1 Memory Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    if all_passed:
        print("\n🎉 V2.1.0 - MEMORY LAYER - ALL TESTS PASSED!")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)