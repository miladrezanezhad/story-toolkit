"""
Main entry point for CLI.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import argparse
import sys

from .commands import story, template, character, dialogue, export, memory, dashboard


def create_parser():
    """Create main argument parser"""
    parser = argparse.ArgumentParser(
        prog='story-toolkit',
        description='Story Development Toolkit - Command Line Interface',
        epilog='Example: story-toolkit new --genre fantasy --theme courage'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Top-level direct shortcuts
    story.add_story_parser(subparsers)

    # Grouped commands
    story_parser = subparsers.add_parser('story', help='Story management')
    story_subparsers = story_parser.add_subparsers(dest='subcommand')
    story.add_story_parser(story_subparsers)

    # Template commands
    template_parser = subparsers.add_parser('template', help='Template management')
    template_subparsers = template_parser.add_subparsers(dest='subcommand')
    template.add_template_parser(template_subparsers)

    # Character commands
    character.add_character_parser(subparsers)

    # Dialogue commands
    dialogue.add_dialogue_parser(subparsers)

    # Export commands
    export.add_export_parser(subparsers)

    # Memory commands
    memory.add_memory_parser(subparsers)

    # Dashboard command
    dashboard.add_dashboard_parser(subparsers)

    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    # Execute command
    result = args.func(args)

    sys.exit(0 if result is not None else 1)


if __name__ == '__main__':
    main()
