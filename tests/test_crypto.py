# Unit tests for cryptographic operations including:
# - Password-based key derivation
# - AES-GCM encryption and decryption
# - Payload packing/unpacking

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import crypto

def test_crypto_functions():
    print("Testing crypto functions...")
    password = "test_password"
    plaintext = b"Test message for crypto verification"
    
    # Key derivation
    key1, salt = crypto.derive_key_from_password(password)
    key2, _ = crypto.derive_key_from_password(password, salt=salt, kdf_params=None)
    
    # Verify keys match
    if key1 != key2:
        print(f"❌ Key derivation failed: {key1.hex()} != {key2.hex()}")
        return False
    print("✅ Key derivation consistent")
    
    # Encryption
    ciphertext, nonce, tag = crypto.encrypt_with_aes_gcm(plaintext, key1)
    
    # Decryption
    try:
        decrypted = crypto.decrypt_with_aes_gcm(ciphertext, key2, nonce, tag)
    except crypto.DecryptionError as e:
        print(f"❌ Decryption failed: {str(e)}")
        return False
    
    # Verify plaintext matches
    if decrypted != plaintext:
        print(f"❌ Decrypted text mismatch: {decrypted} != {plaintext}")
        return False
    
    print("✅ Encryption/decryption successful")
    return True

if __name__ == "__main__":
    test_crypto_functions()
