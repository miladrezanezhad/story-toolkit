"""
Tests for v1.0.0 - Core features

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from .test_core import run_all as test_core
from .test_generators import run_all as test_generators
from .test_nlp import run_all as test_nlp

__all__ = ['test_core', 'test_generators', 'test_nlp']