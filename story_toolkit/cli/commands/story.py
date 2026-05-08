"""
Story commands for CLI.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import json
from story_toolkit import StoryToolkit


def cmd_new(args):
    """Create a new story"""
    try:
        toolkit = StoryToolkit()
        story = toolkit.create_story(
            genre=args.genre,
            theme=args.theme,
            complexity=getattr(args, 'complexity', 3)
        )
        print(f"✅ Story created: {args.genre}/{args.theme}")
        
        # Save to file if output specified
        if hasattr(args, 'output') and args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(story, f, indent=2, ensure_ascii=False)
            print(f"   📁 Saved to {args.output}")
        
        return story
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def cmd_list_stories(args):
    """List all stories in memory"""
    try:
        toolkit = StoryToolkit(memory_backend="sqlite", db_path="stories.db")
        stories = toolkit.list_stored_stories()
        
        if not stories:
            print("📖 No stories found in database")
            return
        
        print(f"\n📚 Found {len(stories)} stories:")
        for story in stories:
            print(f"   📖 {story.name} (ID: {story.id})")
            print(f"      Genre: {story.genre} | Theme: {story.theme}")
        
        toolkit.close_memory()
    except Exception as e:
        print(f"❌ Failed to list stories: {e}")


def add_story_parser(subparsers):
    """Add story subcommands to parser"""
    
    # story new
    parser_new = subparsers.add_parser('new', help='Create a new story')
    parser_new.add_argument('--genre', '-g', required=True, 
                            choices=['fantasy', 'mystery', 'romance', 'adventure', 'sci_fi'],
                            help='Story genre')
    parser_new.add_argument('--theme', '-t', required=True, help='Story theme')
    parser_new.add_argument('--complexity', '-c', type=int, default=3, 
                            choices=[1,2,3,4,5], help='Story complexity (1-5)')
    parser_new.add_argument('--output', '-o', help='Save story to JSON file')
    parser_new.set_defaults(func=cmd_new)
    
    # story list
    parser_list = subparsers.add_parser('list', help='List all stories in memory')
    parser_list.set_defaults(func=cmd_list_stories)