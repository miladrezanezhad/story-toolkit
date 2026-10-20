"""
Export commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
from story_toolkit import StoryToolkit
from story_toolkit.utils.helpers import load_story


def cmd_export(args):
    """Export a story to specified format"""
    try:
        story = None
        if hasattr(args, 'input') and args.input:
            if not os.path.exists(args.input):
                print(f"❌ Input file not found: {args.input}")
                return None
            story = load_story(args.input)
        elif hasattr(args, 'story_id') and args.story_id:
            toolkit = StoryToolkit(memory_backend="sqlite", db_path=getattr(args, 'db', "stories.db"))
            story = toolkit.load_story_from_memory(args.story_id)
            toolkit.close_memory()
        else:
            print("❌ Please specify either an input file (--input) or a stored story ID (--story-id)")
            return None

        toolkit = StoryToolkit()
        output_file = toolkit.export_story(
            story=story,
            format=args.format,
            filename=args.output
        )
        print(f"✅ Story successfully exported to {output_file} (format: {args.format})")
        return output_file
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return None


def add_export_parser(subparsers):
    """Add export subcommands to parser"""
    parser = subparsers.add_parser('export', help='Export story to PDF, EPUB, HTML, JSON, or Markdown')
    parser.add_argument('--format', '-f', required=True,
                        choices=['pdf', 'epub', 'html', 'bionic_html', 'json', 'markdown', 'txt'],
                        help='Export format')
    parser.add_argument('--output', '-o', required=True, help='Output file name or path')
    parser.add_argument('--input', '-i', help='Path to input story JSON file')
    parser.add_argument('--story-id', '-s', help='ID of story in SQLite memory database')
    parser.add_argument('--db', default='stories.db', help='Path to SQLite database (default: stories.db)')
    parser.set_defaults(func=cmd_export)
