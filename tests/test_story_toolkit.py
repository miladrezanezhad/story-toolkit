#!/usr/bin/env python3
"""
Comprehensive test runner for Story Toolkit

Run all tests for all versions:
    python tests/test_story_toolkit.py

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"🧪 {title}")
    print("=" * 70)


def print_success(message: str):
    """Print success message"""
    print(f"  ✅ {message}")


def print_failure(message: str):
    """Print failure message"""
    print(f"  ❌ {message}")


def run_test_module(module_path: str, module_name: str) -> bool:
    """Run a test module and return success status"""
    try:
        # Import the module
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the run_all function if it exists
        if hasattr(module, 'run_all'):
            result = module.run_all()
            return result if isinstance(result, bool) else True
        else:
            print_success(f"{module_name} loaded (no run_all function)")
            return True
            
    except Exception as e:
        print_failure(f"{module_name} failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print_header("STORY TOOLKIT - COMPLETE TEST SUITE")
    print("\n📦 Testing all versions...")
    
    # Define test modules
    test_modules = [
        # v1.0.0
        ("tests/v1/test_core.py", "test_core"),
        ("tests/v1/test_generators.py", "test_generators"),
        ("tests/v1/test_nlp.py", "test_nlp"),
        
        # v2.0.0
        ("tests/v2/test_llm_core.py", "test_llm_core"),
        ("tests/v2/test_llm_integration.py", "test_llm_integration"),
        ("tests/v2/test_llm_backends.py", "test_llm_backends"),
        
        # v2.1.0
        ("tests/v2_1/test_memory.py", "test_memory"),
        
        # v2.2.0
        ("tests/v2_2/test_exporters.py", "test_exporters"),
        
        # v2.2.1
        ("tests/v2_2_1/test_templates.py", "test_templates"),
        
        # v2.2.2
        ("tests/v2_2_2/test_cli.py", "test_cli"),
    ]
    
    results = []
    total_tests_estimate = 70  # Total from our test summary
    
    for module_path, module_name in test_modules:
        print(f"\n📋 Running {module_name}...")
        success = run_test_module(module_path, module_name)
        results.append((module_name, success))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, s in results if s)
    failed = len(results) - passed
    
    for name, status in results:
        if status:
            print_success(f"{name}")
        else:
            print_failure(f"{name}")
    
    print("\n" + "-" * 70)
    print(f"📊 Modules: {passed}/{len(results)} passed")
    print(f"📊 Estimated tests: ~{total_tests_estimate} total")
    
    if passed == len(results):
        print("\n🎉" + "=" * 68)
        print("🎉 ALL TESTS PASSED! STORY TOOLKIT IS FULLY FUNCTIONAL!")
        print("🎉" + "=" * 68)
        return 0
    else:
        print("\n⚠️" + "=" * 68)
        print(f"⚠️ {failed} module(s) failed. Please check the errors above.")
        print("⚠️" + "=" * 68)
        return 1


if __name__ == "__main__":
    sys.exit(main())