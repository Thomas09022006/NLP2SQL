import unittest
import sys
import os

# Add the project root to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(base_dir)

def run_suite():
    print("=" * 60)
    print("CricSQL Backend Unit Test Suite")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    # Discover and load all test files starting with 'test_' in the current directory
    suite = loader.discover(start_dir=os.path.dirname(__file__), pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("Test Execution Summary:")
    print(f"  - Run: {result.testsRun}")
    print(f"  - Errors: {len(result.errors)}")
    print(f"  - Failures: {len(result.failures)}")
    print("=" * 60)
    
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
