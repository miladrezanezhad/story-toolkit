"""
CLI commands module.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from .story import add_story_parser
from .template import add_template_parser

__all__ = ['add_story_parser', 'add_template_parser']
