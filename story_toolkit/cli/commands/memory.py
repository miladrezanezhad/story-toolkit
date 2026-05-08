"""
Memory commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

def add_memory_parser(subparsers):
    """Add memory subcommands to parser"""
    parser = subparsers.add_parser('memory', help='Memory management')
    subparsers = parser.add_subparsers(dest='subcommand')
    
    # memory save
    save_parser = subparsers.add_parser('save', help='Save story to memory')
    save_parser.add_argument('--id', '-i', help='Story ID')
    save_parser.set_defaults(func=lambda args: print("💾 Story saved to memory"))
    
    # memory load
    load_parser = subparsers.add_parser('load', help='Load story from memory')
    load_parser.add_argument('--id', '-i', required=True, help='Story ID')
    load_parser.set_defaults(func=lambda args: print(f"📖 Loading story: {args.id}"))
    
    # memory list
    list_parser = subparsers.add_parser('list', help='List stories in memory')
    list_parser.set_defaults(func=lambda args: print("📚 Stories in memory will be listed here"))
