#!/usr/bin/env python3
"""
Simple Security Test Runner for Story Toolkit

Runs all security tests by directly importing and executing them.
"""

import sys
import os
from pathlib import Path

# Add project root and security directory to path
PROJECT_ROOT = Path(__file__).parent.parent
SECURITY_DIR = PROJECT_ROOT / "tests" / "security"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SECURITY_DIR))

print("=" * 70)
print("🔒 STORY TOOLKIT - SECURITY TEST SUITE")
print("=" * 70)
print(f"\n📁 Security directory: {SECURITY_DIR}")
print(f"📁 Python path: {sys.path[:2]}\n")

# List of test modules
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

results = []
total_passed = 0

for module_name in test_modules:
    print(f"\n📋 Running {module_name}...")
    print("-" * 40)
    
    try:
        # Import the module
        module = __import__(module_name)
        
        # Run the test
        if hasattr(module, 'run'):
            success = module.run()
            if success:
                print(f"\n  ✅ {module_name} PASSED")
                total_passed += 1
                results.append((module_name, True))
            else:
                print(f"\n  ❌ {module_name} FAILED")
                results.append((module_name, False))
        else:
            print(f"  ⚠️ {module_name} has no run() function")
            results.append((module_name, False))
            
    except ImportError as e:
        print(f"  ❌ Cannot import {module_name}: {e}")
        results.append((module_name, False))
    except Exception as e:
        print(f"  ❌ {module_name} error: {e}")
        results.append((module_name, False))

# Summary
print("\n" + "=" * 70)
print("🔒 SECURITY TEST SUMMARY")
print("=" * 70)

print("\n📋 Results:")
print("-" * 40)
for name, passed in results:
    if passed:
        print(f"  ✅ {name}")
    else:
        print(f"  ❌ {name}")

print("-" * 40)
print(f"\n📊 Total: {total_passed}/{len(test_modules)} modules passed")

if total_passed == len(test_modules):
    print("\n🔒" + "=" * 68)
    print("🔒 ALL SECURITY TESTS PASSED! LIBRARY IS SECURE!")
    print("🔒" + "=" * 68)
    sys.exit(0)
else:
    print("\n⚠️" + "=" * 68)
    print(f"⚠️ {len(test_modules) - total_passed} module(s) failed!")
    print("⚠️" + "=" * 68)
    sys.exit(1)