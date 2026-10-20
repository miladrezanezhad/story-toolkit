"""
Memory commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import json
from story_toolkit import StoryToolkit
from story_toolkit.utils.helpers import load_story


def cmd_memory_save(args):
    """Save story file into SQLite memory"""
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=args.db)
        story_data = load_story(args.file)
        meta = story_data.get("metadata", {})
        story_id = toolkit._memory.create_story(
            name=meta.get("name", meta.get("title", "Imported Story")),
            genre=meta.get("genre", "fantasy"),
            theme=meta.get("theme", "adventure"),
            description=meta.get("description", "Imported from file")
        )

        for char in story_data.get("characters", []):
            if isinstance(char, dict):
                toolkit._memory.add_character(
                    story_id=story_id,
                    name=char.get("name", "Unknown"),
                    role=char.get("role", "supporting"),
                    traits=char.get("personality_traits", [])
                )

        toolkit.close_memory()
        print(f"💾 Story saved to memory with ID: {story_id}")
        return story_id
    except Exception as e:
        print(f"❌ Failed to save story to memory: {e}")
        return None


def cmd_memory_load(args):
    """Load and print story from memory"""
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=args.db)
        story = toolkit.load_story_from_memory(args.id)
        toolkit.close_memory()
        print(f"\n📖 Story Loaded: {story['metadata']['name']}")
        print(f"   Genre: {story['metadata']['genre']} | Theme: {story['metadata']['theme']}")
        print(f"   Characters: {len(story['characters'])}")
        return story
    except Exception as e:
        print(f"❌ Failed to load story: {e}")
        return None


def cmd_memory_list(args):
    """List all stories in memory"""
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=args.db)
        stories = toolkit.list_stored_stories()
        toolkit.close_memory()

        if not stories:
            print("📖 No stories found in database.")
            return []

        print(f"\n📚 Stories in memory ({len(stories)}):")
        for s in stories:
            print(f"   - [{s.id}] {s.name} ({s.genre}/{s.theme})")
        return stories
    except Exception as e:
        print(f"❌ Failed to list stories: {e}")
        return []


def add_memory_parser(subparsers):
    """Add memory subcommands to parser"""
    parser = subparsers.add_parser('memory', help='Long-term memory management (SQLite)')
    mem_subparsers = parser.add_subparsers(dest='subcommand')

    # memory save
    save_parser = mem_subparsers.add_parser('save', help='Save story JSON file to memory')
    save_parser.add_argument('--file', '-f', required=True, help='Path to story JSON file')
    save_parser.add_argument('--db', default='stories.db', help='SQLite database path')
    save_parser.set_defaults(func=cmd_memory_save)

    # memory load
    load_parser = mem_subparsers.add_parser('load', help='Load story from memory')
    load_parser.add_argument('--id', '-i', required=True, help='Story ID')
    load_parser.add_argument('--db', default='stories.db', help='SQLite database path')
    load_parser.set_defaults(func=cmd_memory_load)

    # memory list
    list_parser = mem_subparsers.add_parser('list', help='List stories in memory')
    list_parser.add_argument('--db', default='stories.db', help='SQLite database path')
    list_parser.set_defaults(func=cmd_memory_list)
