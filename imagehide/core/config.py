# Configuration constants for ImageHide core functionality

# Steganography constants
STEGANOGRAPHY_START_TAG = "<start_msg>"
STEGANOGRAPHY_END_TAG = "<end_msg>"

# Cryptography constants
CRYPTO_SALT_LENGTH = 16  # 128-bit salt
CRYPTO_NONCE_LENGTH = 12  # 96-bit nonce for AES-GCM
CRYPTO_AUTH_TAG_LENGTH = 16  # 128-bit authentication tag
