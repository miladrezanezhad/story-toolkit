#!/usr/bin/env python3
"""
Launcher for Story Development Toolkit Web Dashboard.

Runs the Gemini-styled creative narrative studio.
Usage:
    python dashboard.py
    python dashboard.py 8080

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from story_toolkit.web.server import run_dashboard

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_dashboard(host="127.0.0.1", port=port, open_browser=True)
