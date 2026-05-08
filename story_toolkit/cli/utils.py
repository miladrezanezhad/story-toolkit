"""
Utility functions for CLI.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import json
import os
from typing import Dict, Any


def save_json(data: Dict[str, Any], filename: str):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(filename: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")


def print_info(message: str):
    """Print info message"""
    print(f"📖 {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"⚠️ {message}")


def print_header(title: str):
    """Print section header"""
    print("\n" + "="*50)
    print(f"📚 {title}")
    print("="*50)
