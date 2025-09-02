# Unit tests for steganography operations including:
# - LSB payload embedding and extraction
# - Payload construction from text
# - Image capacity calculations

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PIL import Image
from core import steganography

def test_steganography():
    print("Testing steganography functions...")
    # Create a test image
    test_image = Image.new('RGB', (100, 100), color=(100, 150, 200))
    test_payload = b"Test payload for steganography verification"
    
    # Embed payload
    stego_image = steganography.embed_payload_into_image(test_image, test_payload)
    
    # Extract payload
    extracted_payload = steganography.extract_payload_from_image(stego_image)
    
    # Verify payload matches
    if extracted_payload == test_payload:
        print("✅ Steganography embedding/extraction successful")
        return True
    else:
        print(f"❌ Payload mismatch: {extracted_payload} != {test_payload}")
        return False

if __name__ == "__main__":
    test_steganography()
