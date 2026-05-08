"""
Main entry point for running examples.

Usage:
    python -m story_toolkit [simple|full|advanced|test]
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "simple"
    
    if command == "simple":
        from examples.simple_example import quick_start
        quick_start()
    elif command == "full":
        from examples.example import main as run_full
        run_full()
    elif command == "advanced":
        from examples.advanced_example import main as run_advanced
        run_advanced()
    elif command == "test":
        from tests.test_core import test_story_engine
        test_story_engine()
        print("Tests passed!")
    else:
        print(f"Unknown command: {command}")
        print("Available: simple, full, advanced, test")

if __name__ == "__main__":
    main()
