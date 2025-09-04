# Text and bit-level encoding utilities.
#
# This module handles conversions between text (Unicode), bytes and bit
# sequences, and performs the simple rotation cipher requested (letter
# rotation by password-dependent shift). It does not perform cryptographic
# encryption — that responsibility belongs to the crypto module.

from typing import List, Iterable

def text_to_bytes(text: str, encoding: str = "utf-8") -> bytes:
    """Encode text to bytes using the chosen character encoding.
    
    :param text: Text string to encode.
    :param encoding: Character encoding (default: 'utf-8').
    :returns: Encoded bytes.
    """
    return text.encode(encoding)

def bytes_to_text(data: bytes, encoding: str = "utf-8") -> str:
    """Decode bytes into text using the chosen character encoding.
    
    :param data: Byte sequence to decode.
    :param encoding: Character encoding (default: 'utf-8').
    :returns: Decoded text string.
    """
    return data.decode(encoding)

def bytes_to_bits(data: bytes) -> List[int]:
    """Convert a bytes object into a list of bits (big-endian per byte).
    
    :param data: Bytes to expand into bits.
    :returns: List of integers 0 or 1.
    """
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits: Iterable[int]) -> bytes:
    """Pack an iterable of bits (0/1) into a bytes object.
    
    :param bits: Iterable yielding bits (0 or 1).
    :returns: Packed bytes.
    """
    byte_array = bytearray()
    byte_value = 0
    bit_count = 0
    
    for bit in bits:
        byte_value = (byte_value << 1) | bit
        bit_count += 1
        if bit_count == 8:
            byte_array.append(byte_value)
            byte_value = 0
            bit_count = 0
    
    # No padding - only complete bytes are returned
    return bytes(byte_array)

def rotate_letters(text: str, shift: int) -> str:
    """Rotate alphabetic characters by the given shift (Caesar-like).
    
    Rotates only standard A-Z/a-z characters and leaves other Unicode 
    characters (including accented characters) untouched.
    
    :param text: Input string.
    :param shift: Integer shift amount; may be positive or negative.
    :returns: Rotated text string.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            base = ord('a')
            rotated = (ord(char) - base + shift) % 26
            if rotated < 0:
                rotated += 26
            result.append(chr(rotated + base))
        elif 'A' <= char <= 'Z':
            base = ord('A')
            rotated = (ord(char) - base + shift) % 26
            if rotated < 0:
                rotated += 26
            result.append(chr(rotated + base))
        else:
            result.append(char)
    return ''.join(result)
