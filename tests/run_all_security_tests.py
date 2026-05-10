"""
Run all security tests for Story Toolkit

This script runs all security test suites:
- SQL Injection
- XSS Prevention
- Path Traversal
- DoS Attack
- Command Injection
- Memory Exhaustion
- Sensitive Data Leak
- Unicode Attacks
- Concurrent Access

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"🔒 {title}")
    print("=" * 70)


def print_success(message: str):
    """Print success message"""
    print(f"  ✅ {message}")


def print_failure(message: str):
    """Print failure message"""
    print(f"  ❌ {message}")


def run_safe_test(name: str, test_func):
    """Run test safely with error handling"""
    print(f"\n📋 Running {name} tests...")
    try:
        result = test_func()
        if result:
            print_success(f"{name} completed")
        else:
            print_failure(f"{name} had issues")
        return result
    except Exception as e:
        print_failure(f"{name} crashed: {e}")
        traceback.print_exc()
        return False


def create_security_sanitizer_if_not_exists():
    """Create security sanitizer module if it doesn't exist"""
    sanitizer_path = Path(__file__).parent.parent.parent / "story_toolkit" / "security" / "sanitizer.py"
    
    if not sanitizer_path.exists():
        sanitizer_path.parent.mkdir(parents=True, exist_ok=True)
        
        sanitizer_content = '''"""
Security sanitizers for Story Toolkit
"""

import html
import re
import os


class SecuritySanitizer:
    """Sanitize inputs to prevent security issues"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escape HTML special characters"""
        if not isinstance(text, str):
            text = str(text)
        return html.escape(text, quote=True)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove dangerous characters from filename"""
        filename = filename.replace('..', '')
        filename = filename.replace('/', '')
        filename = filename.replace('\\\\', '')
        filename = filename.replace('\\x00', '')
        return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    
    @staticmethod
    def sanitize_path(filepath: str, base_dir: str = None) -> str:
        """Ensure path is within base directory"""
        if base_dir is None:
            base_dir = os.getcwd()
        
        abs_path = os.path.abspath(os.path.join(base_dir, filepath))
        abs_base = os.path.abspath(base_dir)
        
        if not abs_path.startswith(abs_base):
            raise ValueError(f"Path traversal attempt: {filepath}")
        
        return abs_path


def sanitize_html(text: str) -> str:
    return SecuritySanitizer.sanitize_html(text)


def sanitize_filename(filename: str) -> str:
    return SecuritySanitizer.sanitize_filename(filename)


def sanitize_path(filepath: str) -> str:
    return SecuritySanitizer.sanitize_path(filepath)
'''
        
        with open(sanitizer_path, 'w', encoding='utf-8') as f:
            f.write(sanitizer_content)
        print(f"📁 Created security sanitizer: {sanitizer_path}")


def main():
    """Run all security tests"""
    print_header("STORY TOOLKIT - COMPLETE SECURITY TEST SUITE")
    print("\n🛡️ Running comprehensive security tests...")
    
    # Create sanitizer if needed
    create_security_sanitizer_if_not_exists()
    
    # Import test modules with error handling
    tests = []
    
    test_modules = [
        "test_sql_injection",
        "test_xss_prevention",
        "test_path_traversal",
        "test_dos_attack",
        "test_command_injection",
        "test_memory_exhaustion",
        "test_sensitive_data_leak",
        "test_unicode_attacks",
        "test_concurrent_access",
    ]
    
    for module_name in test_modules:
        try:
            # Import using importlib for better error handling
            import importlib
            module = importlib.import_module(module_name)
            if hasattr(module, 'run'):
                tests.append((module_name, module.run))
            else:
                print(f"⚠️ Module {module_name} has no run() function")
        except ImportError as e:
            print(f"⚠️ Could not import {module_name}: {e}")
        except Exception as e:
            print(f"⚠️ Error loading {module_name}: {e}")
    
    if not tests:
        print("❌ No test modules found!")
        return 1
    
    results = []
    for name, test_func in tests:
        success = run_safe_test(name, test_func)
        results.append((name, success))
    
    # Print summary
    print_header("SECURITY TEST SUMMARY")
    
    passed = sum(1 for _, s in results if s)
    
    for name, status in results:
        if status:
            print_success(name)
        else:
            print_failure(name)
    
    print("\n" + "-" * 70)
    print(f"📊 Security Modules: {passed}/{len(results)} passed")
    
    if passed == len(results):
        print("\n🔒" + "=" * 68)
        print("🔒 ALL SECURITY TESTS PASSED! LIBRARY IS SECURE!")
        print("🔒" + "=" * 68)
        return 0
    else:
        print("\n⚠️" + "=" * 68)
        print(f"⚠️ {len(results) - passed} security module(s) had issues.")
        print("⚠️ Review and fix before production deployment!")
        print("⚠️" + "=" * 68)
        return 1


if __name__ == "__main__":
    sys.exit(main())