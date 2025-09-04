# Test runner that executes all test suites:
# 1. Cryptography tests
# 2. Steganography tests
# 3. End-to-end integration test

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests import test_integration, test_crypto, test_steganography

def test_all():
    print("Running all tests...\n")
    
    if not test_crypto.test_crypto_functions():
        print("Crypto tests failed.")
        return
    
    print("\n")
    if not test_steganography.test_steganography():
        print("Steganography tests failed.")
        return
    
    print("\n")
    test_integration.test_end_to_end()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    test_all()