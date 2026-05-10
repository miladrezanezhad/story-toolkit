"""
Security tests for Story Toolkit

This package contains comprehensive security tests:
- SQL Injection (6 tests)
- XSS Prevention (8 tests)
- Path Traversal (9 tests)
- DoS Attack (9 tests)
- Command Injection (9 tests)
- Memory Exhaustion (9 tests)
- Sensitive Data Leak (8 tests)
- Unicode Attacks (10 tests)
- Concurrent Access (8 tests)

Total: 76 security tests
"""

from .test_sql_injection import test_sql_injection
from .test_xss_prevention import test_xss_prevention
from .test_path_traversal import test_path_traversal
from .test_dos_attack import test_dos_attack
from .test_command_injection import test_command_injection
from .test_memory_exhaustion import test_memory_exhaustion
from .test_sensitive_data_leak import test_sensitive_data_leak
from .test_unicode_attacks import test_unicode_attacks
from .test_concurrent_access import test_concurrent_access

# Version info
__version__ = "1.0.0"
__total_tests__ = 76

# Export test module names
__all__ = [
    'test_sql_injection',
    'test_xss_prevention',
    'test_path_traversal',
    'test_dos_attack',
    'test_command_injection',
    'test_memory_exhaustion',
    'test_sensitive_data_leak',
    'test_unicode_attacks',
    'test_concurrent_access',
]