"""
Export commands for CLI

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

def add_export_parser(subparsers):
    """Add export subcommands to parser"""
    parser = subparsers.add_parser('export', help='Export story')
    parser.add_argument('--format', '-f', required=True, choices=['pdf', 'epub', 'html', 'json'], help='Export format')
    parser.add_argument('--output', '-o', required=True, help='Output file name')
    parser.set_defaults(func=lambda args: print(f"📄 Exporting to {args.output} (format: {args.format})"))