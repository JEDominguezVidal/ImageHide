# Cryptographic primitives and payload packaging for ImageHide.
#
# This module encapsulates password-based key derivation (KDF) and
# symmetric encryption (AES-GCM) as the primary confidentiality layer.
# It also provides pack/unpack helpers for carrying KDF salt, nonce
# and authentication tag together with ciphertext.

import os
from typing import Tuple, Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag
from imagehide.core.errors import DecryptionError

# Constants
SALT_LENGTH = 16  # 128-bit salt
NONCE_LENGTH = 12  # 96-bit nonce for AES-GCM
TAG_LENGTH = 16    # 128-bit authentication tag

def derive_key_from_password(password: str, salt: Optional[bytes] = None, kdf_params: Optional[dict] = None) -> Tuple[bytes, bytes]:
    """Derive a symmetric key from a textual password using PBKDF2.
    
    :param password: Password string provided by the user.
    :param salt: Optional salt bytes; if None a new random salt is generated.
    :param kdf_params: Optional dictionary overriding KDF parameters.
    :returns: Tuple (key, salt).
    """
    # Set KDF parameters with defaults
    iterations = kdf_params.get('iterations', 100000) if kdf_params else 100000
    length = kdf_params.get('length', 32) if kdf_params else 32  # 256-bit key
    
    # Generate new salt if not provided
    if salt is None:
        salt = os.urandom(SALT_LENGTH)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    
    key = kdf.derive(password.encode('utf-8'))
    return key, salt

def encrypt_with_aes_gcm(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
    """Encrypt plaintext with AES-GCM.
    
    :param plaintext: Plaintext bytes to encrypt.
    :param key: Symmetric key bytes (must be 16, 24 or 32 bytes).
    :returns: Tuple (ciphertext, nonce, tag).
    """
    # Generate random nonce
    nonce = os.urandom(NONCE_LENGTH)
    
    # Create cipher and encrypt
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return ciphertext, nonce, encryptor.tag

def decrypt_with_aes_gcm(ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
    """Decrypt AES-GCM ciphertext and verify authenticity.
    
    :param ciphertext: Ciphertext bytes.
    :param key: Symmetric key bytes.
    :param nonce: Nonce used during encryption.
    :param tag: Authentication tag from encryption.
    :returns: Decrypted plaintext bytes.
    :raises: DecryptionError if authentication fails.
    """
    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext
    except InvalidTag as e:
        raise DecryptionError(cause=e)

def pack_encrypted_payload(salt: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    """Pack salt, nonce, tag and ciphertext into a single, versioned blob.
    
    Format: [salt (16)][nonce (12)][tag (16)][ciphertext (variable)]
    
    :param salt: KDF salt bytes (16 bytes).
    :param nonce: AES-GCM nonce (12 bytes).
    :param tag: AES-GCM authentication tag (16 bytes).
    :param ciphertext: Ciphertext bytes.
    :returns: Packed payload bytes.
    """
    if len(salt) != SALT_LENGTH:
        raise ValueError(f"Salt must be {SALT_LENGTH} bytes")
    if len(nonce) != NONCE_LENGTH:
        raise ValueError(f"Nonce must be {NONCE_LENGTH} bytes")
    if len(tag) != TAG_LENGTH:
        raise ValueError(f"Tag must be {TAG_LENGTH} bytes")
    
    return salt + nonce + tag + ciphertext

def unpack_encrypted_payload(payload: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
    """Unpack a payload produced by pack_encrypted_payload.
    
    :param payload: Packed payload bytes.
    :returns: (salt, nonce, tag, ciphertext)
    :raises: ValueError if payload is malformed.
    """
    if len(payload) < SALT_LENGTH + NONCE_LENGTH + TAG_LENGTH:
        raise ValueError("Payload too short to contain required components")
    
    salt = payload[:SALT_LENGTH]
    nonce = payload[SALT_LENGTH:SALT_LENGTH+NONCE_LENGTH]
    tag = payload[SALT_LENGTH+NONCE_LENGTH:SALT_LENGTH+NONCE_LENGTH+TAG_LENGTH]
    ciphertext = payload[SALT_LENGTH+NONCE_LENGTH+TAG_LENGTH:]
    
    return salt, nonce, tag, ciphertext
