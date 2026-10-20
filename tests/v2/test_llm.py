"""
Test runner for all v2 LLM tests.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.v2 import test_llm_core, test_llm_backends, test_llm_integration


def main():
    print("=" * 70)
    print("🚀 RUNNING ALL V2 LLM TEST SUITES")
    print("=" * 70)

    success = True

    try:
        if hasattr(test_llm_core, 'run_all'):
            res = test_llm_core.run_all()
            if res is False:
                success = False
    except Exception as e:
        print(f"❌ Error in test_llm_core: {e}")
        success = False

    try:
        if hasattr(test_llm_backends, 'run_all'):
            res = test_llm_backends.run_all()
            if res is False:
                success = False
    except Exception as e:
        print(f"❌ Error in test_llm_backends: {e}")
        success = False

    try:
        if hasattr(test_llm_integration, 'run_all'):
            res = test_llm_integration.run_all()
            if res is False:
                success = False
    except Exception as e:
        print(f"❌ Error in test_llm_integration: {e}")
        success = False

    if success:
        print("\n🎉 All v2 LLM test suites passed!")
        return 0
    else:
        print("\n❌ Some v2 LLM tests failed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
