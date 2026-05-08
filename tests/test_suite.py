"""
Comprehensive test suite for all versions of Story Toolkit.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_version(version_name, module_path):
    """Run a specific version test module"""
    print(f"\n{'='*60}")
    print(f"RUNNING {version_name}")
    print(f"{'='*60}")
    
    try:
        # Import and run the module's run_all function
        import importlib.util
        spec = importlib.util.spec_from_file_location(version_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'run_all'):
            return module.run_all()
        else:
            print(f"⚠️ No run_all() function in {version_name}")
            return False
    except Exception as e:
        print(f"❌ Failed to run {version_name}: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("🧪 STORY TOOLKIT - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nTesting all versions from v1.0.0 to v2.2.0")
    
    versions = [
        ("V1.0.0 - Core", Path(__file__).parent / "v1" / "test_core.py"),
        ("V2.0.0 - LLM Layer", Path(__file__).parent / "v2" / "test_llm.py"),
        ("V2.1.0 - Memory", Path(__file__).parent / "v2_1" / "test_memory.py"),
        ("V2.2.0 - Exporters", Path(__file__).parent / "v2_2" / "test_exporters.py"),
    ]
    
    results = []
    for name, path in versions:
        if path.exists():
            passed = run_version(name, path)
            results.append((name, passed))
        else:
            print(f"\n⚠️ {name} - test file not found: {path}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 FINAL SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    for name, passed in results:
        print(f"  {'✅' if passed else '❌'} {name}")
    
    print("-"*70)
    print(f"\n📈 Total: {passed_count}/{total_count} test suites passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! Story Toolkit is ready for release!")
    else:
        print(f"\n⚠️ {total_count - passed_count} test suite(s) failed. Please check the errors above.")
    
    print("="*70 + "\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)