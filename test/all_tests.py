import unittest
import os

def discover_and_run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    test_dir = os.path.dirname(os.path.abspath(__file__))

    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.startswith('test') and file.endswith('.py'):
                module_name = os.path.splitext(file)[0]
                module_path = os.path.relpath(os.path.join(root, file), test_dir).replace(os.sep, '.')[:-3]
                try:
                    module = __import__(module_path, fromlist=[module_name])
                    suite.addTests(loader.loadTestsFromModule(module))
                except Exception as e:
                    print(f"Failed to import {module_path}: {e}")

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    if not result.wasSuccessful():
        for failed_test, traceback in result.failures:
            print(f"Test failed: {failed_test.id()}\n{traceback}")

if __name__ == "__main__":
    discover_and_run_tests()