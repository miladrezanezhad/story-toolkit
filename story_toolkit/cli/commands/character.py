"""
Character commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from story_toolkit import Character, CharacterGenerator, StoryToolkit


def cmd_add_character(args):
    """Add a character to a story in memory or create a new character"""
    try:
        char = Character(name=args.name, role=args.role)
        if hasattr(args, 'trait') and args.trait:
            for t in args.trait:
                char.add_trait(t)

        if hasattr(args, 'story_id') and args.story_id:
            toolkit = StoryToolkit(memory_backend="sqlite", db_path=getattr(args, 'db', "stories.db"))
            toolkit._current_story_id = args.story_id
            toolkit._memory.add_character(
                story_id=args.story_id,
                name=char.name,
                role=char.role,
                traits=char.personality_traits
            )
            toolkit.close_memory()
            print(f"✅ Character '{args.name}' added to story {args.story_id}")
        else:
            print(f"✅ Character created: {char.name} ({char.role})")
            if char.personality_traits:
                print(f"   Traits: {', '.join(char.personality_traits)}")
        return char
    except Exception as e:
        print(f"❌ Failed to add character: {e}")
        return None


def cmd_list_characters(args):
    """List characters for a story in memory"""
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path=getattr(args, 'db', "stories.db"))
        if hasattr(args, 'story_id') and args.story_id:
            chars = toolkit._memory.get_characters(args.story_id)
            print(f"\n🎭 Characters in story {args.story_id}:")
            for c in chars:
                print(f"   - {c.name} ({c.role}): {', '.join(c.traits) if c.traits else 'no traits'}")
        else:
            print("❌ Please specify --story-id")
        toolkit.close_memory()
    except Exception as e:
        print(f"❌ Failed to list characters: {e}")


def add_character_parser(subparsers):
    """Add character subcommands to parser"""
    parser = subparsers.add_parser('character', help='Character management')
    char_subparsers = parser.add_subparsers(dest='subcommand')

    # character add
    add_parser = char_subparsers.add_parser('add', help='Add a character')
    add_parser.add_argument('--name', '-n', required=True, help='Character name')
    add_parser.add_argument('--role', '-r', required=True, help='Character role (protagonist, antagonist, etc.)')
    add_parser.add_argument('--trait', '-t', action='append', help='Character trait (repeatable)')
    add_parser.add_argument('--story-id', '-s', help='Optional Story ID to attach character to')
    add_parser.add_argument('--db', default='stories.db', help='SQLite database path')
    add_parser.set_defaults(func=cmd_add_character)

    # character list
    list_parser = char_subparsers.add_parser('list', help='List characters for a story')
    list_parser.add_argument('--story-id', '-s', required=True, help='Story ID')
    list_parser.add_argument('--db', default='stories.db', help='SQLite database path')
    list_parser.set_defaults(func=cmd_list_characters)
