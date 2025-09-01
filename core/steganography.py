# LSB Steganography Engine for ImageHide
#
# This module implements the core steganography operations for embedding and
# extracting messages in images using the Least Significant Bit (LSB) technique.
# Key functionality includes:
# - Payload embedding with size header for accurate extraction
# - Payload extraction using the embedded size header
# - Construction of encrypted payloads from text (with tags and encryption)
# - Recovery of text from extracted encrypted payloads
# - Image channel processing for grayscale and color images
# - Capacity calculation and validation

import struct
from typing import Optional, Tuple, Iterable, Iterator, List
from PIL import Image
from . import crypto, encoding
from .errors import CapacityError, FormatError, DecryptionError

# Constants for message tags
START_TAG = "<start_msg>"
END_TAG = "<end_msg>"
TAG_LENGTH = len(START_TAG) + len(END_TAG)

def embed_payload_into_image(image: Image.Image, payload: bytes, include_alpha: bool = False, lsb_count: int = 1) -> Image.Image:
    """Embed the given payload bytes into the image's least-significant bits.
    
    The embedding is performed by mapping bits from `payload` into the
    LSBs of the image's pixel channel bytes in a deterministic order.
    The mapping is row-major (y from 0..height-1, x from 0..width-1) and
    uses the canonical channel ordering for the image mode (for example
    'RGB' -> R,G,B). The function returns a new PIL Image instance with
    the modified pixels; the original Image object must not be mutated.

    :param image: Source PIL Image instance.
    :param payload: Bytes to embed (with start/end tags).
    :param include_alpha: Whether to include the alpha channel.
    :param lsb_count: Number of least-significant bits to use per channel.
    :returns: New PIL Image instance with embedded payload.
    :raises: CapacityError if the image lacks sufficient LSB capacity.
    """
    # Prepend payload length header (4 bytes)
    payload_with_header = struct.pack('>I', len(payload)) + payload
    
    # Calculate required bits and available capacity
    required_bits = calculate_required_bits_for_payload(len(payload_with_header), lsb_count)
    available_bits = image.width * image.height * (3 if include_alpha else 4) * lsb_count
    
    if required_bits > available_bits:
        raise CapacityError(required_bits, available_bits)
    
    # Convert payload to bits
    payload_bits = list(encoding.bytes_to_bits(payload_with_header))
    
    # Create mask for LSB manipulation
    lsb_mask = (1 << lsb_count) - 1
    clear_mask = 0xFF ^ lsb_mask
    
    # Process image channels
    modified_channels = []
    channel_iter = _iter_channel_bytes(image, include_alpha)
    bit_index = 0
    
    for channel_byte in channel_iter:
        if bit_index < len(payload_bits):
            # Clear existing LSBs
            cleaned_byte = channel_byte & clear_mask
            # Get next payload bits
            payload_value = 0
            for i in range(lsb_count):
                if bit_index < len(payload_bits):
                    payload_value |= (payload_bits[bit_index] << i)
                    bit_index += 1
            # Set new LSBs
            modified_byte = cleaned_byte | payload_value
            modified_channels.append(modified_byte)
        else:
            modified_channels.append(channel_byte)
    
    return _channels_to_image(image, modified_channels, include_alpha)

def extract_payload_from_image(image: Image.Image, include_alpha: bool = False, lsb_count: int = 1) -> bytes:
    """Extract a packed payload from the image by reading LSBs.
    
    The function reads LSBs from the image channels in the same
    deterministic order used by `embed_payload_into_image`, reconstructs
    the bitstream and returns the resulting packed payload bytes.

    :param image: PIL Image instance containing an embedded payload.
    :param include_alpha: Whether the embedding used the alpha channel.
    :param lsb_count: Number of LSBs per channel that were used.
    :returns: Extracted packed payload bytes.
    :raises: FormatError if a valid payload cannot be located.
    """
    # Extract bits from image channels
    extracted_bits = []
    for channel_byte in _iter_channel_bytes(image, include_alpha):
        # Extract LSBs
        for i in range(lsb_count):
            extracted_bits.append((channel_byte >> i) & 1)
    
    # Convert bits to bytes
    payload_with_header = encoding.bits_to_bytes(extracted_bits)
    
    # Extract payload length from header
    if len(payload_with_header) < 4:
        raise FormatError("Payload header missing or corrupted")
    
    payload_length = struct.unpack('>I', payload_with_header[:4])[0]
    
    # Verify payload length
    if len(payload_with_header) < 4 + payload_length:
        raise FormatError("Payload length mismatch")
    
    return payload_with_header[4:4+payload_length]

def build_payload_from_text(text: str, password: str, kdf_params: Optional[dict] = None) -> bytes:
    """Create the final packed payload bytes from plaintext and a password.
    
    This performs the full prepare-and-pack pipeline:
    1. Add start/end tags to the message
    2. Rotate letters based on password
    3. Encode text to UTF-8 bytes
    4. Encrypt with AES-GCM
    5. Pack salt, nonce, tag and ciphertext

    :param text: Plaintext message to protect.
    :param password: Password string used for rotation and key derivation.
    :param kdf_params: Optional dictionary overriding KDF parameters.
    :returns: Packed payload bytes ready for embedding.
    """
    # Add tags to message
    tagged_text = f"{START_TAG}{text}{END_TAG}"
    
    # Apply rotation cipher
    shift = len(password)
    rotated_text = encoding.rotate_letters(tagged_text, shift)
    
    # Encode to UTF-8
    utf8_bytes = encoding.text_to_bytes(rotated_text, "utf-8")
    
    # Derive encryption key
    key, salt = crypto.derive_key_from_password(password, kdf_params=kdf_params)
    
    # Encrypt message
    ciphertext, nonce, tag = crypto.encrypt_with_aes_gcm(utf8_bytes, key)
    
    # Pack payload
    return crypto.pack_encrypted_payload(salt, nonce, tag, ciphertext)

def extract_text_from_payload(payload: bytes, password: str) -> str:
    """Recover the plaintext text from a packed payload using the password.
    
    This reverses the work performed by build_payload_from_text:
    1. Unpack the payload
    2. Derive symmetric key
    3. Decrypt ciphertext
    4. Decode UTF-8 bytes
    5. Reverse rotation
    6. Remove tags

    :param payload: Packed payload bytes extracted from an image.
    :param password: Password used for decryption and rotation reversal.
    :returns: Recovered plaintext string.
    :raises: DecryptionError if authentication fails or password is incorrect.
    """
    # Unpack payload
    salt, nonce, tag, ciphertext = crypto.unpack_encrypted_payload(payload)
    
    # Derive key using the same parameters as encryption (kdf_params=None)
    key, _ = crypto.derive_key_from_password(password, salt=salt, kdf_params=None)
    
    # Decrypt
    decrypted_bytes = crypto.decrypt_with_aes_gcm(ciphertext, key, nonce, tag)
    
    # Decode UTF-8
    decoded_text = encoding.bytes_to_text(decrypted_bytes, "utf-8")
    
    # Reverse rotation
    shift = -len(password)
    derotated_text = encoding.rotate_letters(decoded_text, shift)
    
    # Remove tags
    if derotated_text.startswith(START_TAG) and derotated_text.endswith(END_TAG):
        return derotated_text[len(START_TAG):-len(END_TAG)]
    raise FormatError("Payload tags are missing or corrupted")

def calculate_required_bits_for_payload(payload_length_bytes: int, lsb_count: int = 1) -> int:
    """Return number of LSB bits required to embed a payload of given size.
    
    :param payload_length_bytes: Size of the packed payload in bytes.
    :param lsb_count: Number of LSBs used per channel.
    :returns: Number of LSB bits required.
    """
    return payload_length_bytes * 8

def _iter_channel_bytes(image: Image.Image, include_alpha: bool = False) -> Iterator[int]:
    """Yield the numeric channel byte values for each pixel in row-major order."""
    pixels = image.load()
    width, height = image.size
    mode = image.mode
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if isinstance(pixel, int):
                # Grayscale image
                yield pixel
            else:
                # Color image (RGB, RGBA, etc.)
                for i, channel in enumerate(pixel):
                    if include_alpha or (mode != 'RGBA' and mode != 'LA') or i < len(pixel) - 1:
                        yield channel

def _channels_to_image(image: Image.Image, modified_channels: Iterable[int], include_alpha: bool = False) -> Image.Image:
    """Rebuild a PIL Image from an iterable of modified channel bytes."""
    width, height = image.size
    mode = image.mode
    new_image = Image.new(mode, (width, height))
    pixels = new_image.load()
    
    channel_iter = iter(modified_channels)
    
    for y in range(height):
        for x in range(width):
            if mode in ['L', '1']:  # Grayscale
                pixels[x, y] = next(channel_iter)
            else:
                num_channels = 4 if mode == 'RGBA' else 3
                pixel = []
                for _ in range(num_channels):
                    if include_alpha or (len(pixel) < num_channels - 1) or num_channels == 3:
                        pixel.append(next(channel_iter))
                    else:
                        # Keep original alpha channel if not included
                        pixel.append(original_pixel[3])
                pixels[x, y] = tuple(pixel)
    
    return new_image
