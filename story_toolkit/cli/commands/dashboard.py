"""
Dashboard command for Story Toolkit CLI.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys


def cmd_dashboard(args):
    """Launch the Gemini-styled Web Dashboard"""
    from story_toolkit.web.server import run_dashboard
    port = getattr(args, 'port', 8080)
    no_browser = getattr(args, 'no_browser', False)
    run_dashboard(host="127.0.0.1", port=port, open_browser=not no_browser)


def add_dashboard_parser(subparsers):
    """Add dashboard subcommand to parser"""
    parser = subparsers.add_parser('dashboard', help='Launch Gemini-style Web Dashboard')
    parser.add_argument('--port', '-p', type=int, default=8080, help='Port to run web server on (default: 8080)')
    parser.add_argument('--no-browser', action='store_true', help='Do not automatically open web browser')
    parser.set_defaults(func=cmd_dashboard)
