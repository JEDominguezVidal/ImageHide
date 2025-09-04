# Core module initialisation.
#
# This package contains the core building blocks: I/O helpers, encoding
# utilities, cryptographic primitives, and the steganography engine.
# Consumers should import the public functions from these submodules rather
# than reaching into private implementation details.

from imagehide.core.image_io import load_image, save_image
from imagehide.core.steganography import embed_payload_into_image, extract_payload_from_image
from imagehide.core.crypto import derive_key_from_password, encrypt_with_aes_gcm, decrypt_with_aes_gcm

__all__ = [
    "load_image",
    "save_image",
    "embed_payload_into_image",
    "extract_payload_from_image",
    "derive_key_from_password",
    "encrypt_with_aes_gcm",
    "decrypt_with_aes_gcm",
]