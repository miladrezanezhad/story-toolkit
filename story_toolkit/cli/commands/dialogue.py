"""
Dialogue commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

def add_dialogue_parser(subparsers):
    """Add dialogue subcommands to parser"""
    parser = subparsers.add_parser('dialogue', help='Dialogue generation')
    parser.add_argument('--speaker', '-s', required=True, help='Speaker name')
    parser.add_argument('--listener', '-l', required=True, help='Listener name')
    parser.add_argument('--context', '-c', default='conflict', help='Dialogue context')
    parser.add_argument('--lines', '-n', type=int, default=5, help='Number of lines')
    parser.set_defaults(func=lambda args: print(f"💬 Dialogue between {args.speaker} and {args.listener}"))