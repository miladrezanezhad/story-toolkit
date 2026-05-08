"""
Character commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

def add_character_parser(subparsers):
    """Add character subcommands to parser"""
    parser = subparsers.add_parser('character', help='Character management')
    subparsers = parser.add_subparsers(dest='subcommand')
    
    # character add
    add_parser = subparsers.add_parser('add', help='Add a character')
    add_parser.add_argument('--name', '-n', required=True, help='Character name')
    add_parser.add_argument('--role', '-r', required=True, help='Character role')
    add_parser.add_argument('--trait', '-t', action='append', help='Character trait')
    add_parser.set_defaults(func=lambda args: print(f"✅ Character '{args.name}' added"))
    
    # character list
    list_parser = subparsers.add_parser('list', help='List characters')
    list_parser.set_defaults(func=lambda args: print("📖 Characters will be listed here"))
