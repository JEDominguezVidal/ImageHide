# Image I/O helpers.
#
# This module provides functions to load and save images, inspect their
# channel layout (grayscale vs colour), convert to/from byte or numeric
# arrays suitable for bit-level manipulation, and compute storage capacity
# (in bits / characters) for a given image when using LSB steganography.

import os
from typing import Tuple, Optional
from PIL import Image
from imagehide.core.errors import FormatError

def load_image(path: str) -> Image.Image:
    """Load an image from the filesystem and return a PIL Image object.

    :param path: Path to the image file.
    :returns: PIL Image instance representing the loaded image.
    :raises: FormatError if file doesn't exist or is unreadable.
    """
    if not os.path.exists(path):
        raise FormatError(f"Image file not found: {path}")
    try:
        return Image.open(path)
    except Exception as e:
        raise FormatError(f"Error loading image: {str(e)}")

def save_image(image: Image.Image, path: str, optimise: bool = True, format: Optional[str] = None) -> None:
    """Save a PIL Image to disk.

    :param image: PIL Image instance to save.
    :param path: Destination path.
    :param optimise: Whether to attempt to optimise the output file.
    :param format: Optional explicit format (e.g. 'PNG', 'BMP').
    :returns: None
    """
    if format is None:
        # Determine format from file extension
        ext = os.path.splitext(path)[1][1:].upper()
        format = ext if ext in ['PNG', 'BMP', 'TIFF'] else 'PNG'
    
    image.save(path, format=format, optimize=optimise)

def is_grayscale(image: Image.Image) -> bool:
    """Return True if the image uses a single greyscale channel.

    :param image: PIL Image instance.
    :returns: Boolean indicating whether the image is greyscale.
    """
    return image.mode in ['L', 'LA', '1']

def get_num_channels(image: Image.Image, include_alpha: bool = False) -> int:
    """Return the number of usable channels for embedding.

    :param image: PIL Image instance.
    :param include_alpha: Whether to treat the alpha channel as usable.
    :returns: Number of usable channels.
    """
    mode = image.mode
    if mode in ['L', '1']:  # Grayscale
        return 1
    elif mode == 'RGB':
        return 3
    elif mode == 'RGBA':
        return 4 if include_alpha else 3
    elif mode == 'CMYK':
        return 4
    elif mode == 'YCbCr':
        return 3
    elif mode == 'LAB':
        return 3
    elif mode == 'HSV':
        return 3
    else:
        # Fallback to number of bands
        return len(image.getbands()) if include_alpha else len(image.getbands()) - 1

def get_capacity_bits(image: Image.Image, include_alpha: bool = False, lsb_count: int = 1) -> int:
    """Return the number of bits available for LSB embedding.

    :param image: PIL Image instance.
    :param include_alpha: Whether to count the alpha channel.
    :param lsb_count: Number of LSBs to use per channel.
    :returns: Integer number of available bits.
    """
    num_channels = get_num_channels(image, include_alpha)
    return image.width * image.height * num_channels * lsb_count

def get_capacity_chars(image: Image.Image, include_alpha: bool = False, char_encoding: str = "utf-8", lsb_count: int = 1) -> int:
    """Return approximate number of characters that fit in the image.

    :param image: PIL Image instance.
    :param include_alpha: Whether to count the alpha channel.
    :param char_encoding: Character encoding used for estimation.
    :param lsb_count: Number of LSBs to use per channel.
    :returns: Approximate number of characters.
    """
    # Estimate average bytes per character (UTF-8: 1-4 bytes, average ~1.1 for English)
    avg_bytes_per_char = 1.5 if char_encoding.lower() == "utf-8" else 2.0
    
    # Calculate total bits available
    total_bits = get_capacity_bits(image, include_alpha, lsb_count)
    
    # Convert to bytes and divide by average bytes per character
    return int(total_bits / (8 * avg_bytes_per_char))

def image_to_raw_bytes(image: Image.Image, include_alpha: bool = False) -> bytes:
    """Return raw pixel bytes in a deterministic channel order.

    :param image: PIL Image instance.
    :param include_alpha: Whether to include alpha channel bytes.
    :returns: Raw bytes representing pixel channels.
    """
    # Convert image to RGBA if it's not already in a compatible mode
    if image.mode not in ['L', 'LA', 'RGB', 'RGBA']:
        image = image.convert('RGBA')
    
    # Get pixel data
    pixels = image.tobytes()
    
    # Process based on image mode
    if image.mode == 'L':  # Grayscale
        return pixels
    elif image.mode == 'LA':  # Grayscale with alpha
        if include_alpha:
            return pixels
        else:
            # Remove alpha channel (keep luminance only) by taking every other byte
            return pixels[::2]
    elif image.mode == 'RGB':
        return pixels
    elif image.mode == 'RGBA':
        if include_alpha:
            return pixels
        else:
            # Remove alpha channel (keep RGB only)
            result = bytearray()
            for i in range(0, len(pixels), 4):
                result.extend(pixels[i:i+3])  # Take RGB bytes, skip alpha
            return bytes(result)
            
def raw_bytes_to_image(raw: bytes, size: Tuple[int, int], mode: str) -> Image.Image:
    """Recreate a PIL Image from raw pixel bytes.

    :param raw: Raw pixel bytes in the same ordering used by image_to_raw_bytes.
    :param size: (width, height) tuple.
    :param mode: PIL mode string (e.g. 'RGB', 'L').
    :returns: PIL Image instance.
    """
    return Image.frombytes(mode, size, raw)
