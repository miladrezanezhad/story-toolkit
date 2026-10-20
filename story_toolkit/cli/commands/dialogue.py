"""
Dialogue commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from story_toolkit import StoryToolkit, LLMFactory, LLMProvider


def cmd_dialogue(args):
    """Generate dialogue between two characters"""
    try:
        toolkit = StoryToolkit()
        dialogue = toolkit.dialogue_gen.generate_dialogue(
            speaker=args.speaker,
            listener=args.listener,
            context=getattr(args, 'context', 'conflict'),
            num_lines=getattr(args, 'lines', 5)
        )

        print(f"\n💬 Dialogue between {args.speaker} and {args.listener} ({args.context}):")
        print("=" * 60)
        for line in dialogue:
            print(f"   {line}")
        print("=" * 60)
        return dialogue
    except Exception as e:
        print(f"❌ Failed to generate dialogue: {e}")
        return None


def add_dialogue_parser(subparsers):
    """Add dialogue subcommands to parser"""
    parser = subparsers.add_parser('dialogue', help='Dialogue generation')
    parser.add_argument('--speaker', '-s', required=True, help='Speaker name')
    parser.add_argument('--listener', '-l', required=True, help='Listener name')
    parser.add_argument('--context', '-c', default='conflict',
                        choices=['conflict', 'revelation', 'emotional', 'romantic', 'action', 'mystery'],
                        help='Dialogue context')
    parser.add_argument('--lines', '-n', type=int, default=5, help='Number of lines (default: 5)')
    parser.set_defaults(func=cmd_dialogue)
