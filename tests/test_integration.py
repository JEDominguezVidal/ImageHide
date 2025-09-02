# End-to-end integration test for ImageHide workflow:
# 1. Message encoding with password protection
# 2. Payload embedding into image
# 3. Payload extraction and decryption
# 4. Verification of original message recovery

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
from PIL import Image
import numpy as np
from core import steganography, image_io

def test_end_to_end():
    print("Starting ImageHide integration test...")
    
    # Create a test image
    width, height = 100, 100
    test_image = Image.new('RGB', (width, height), color=(50, 100, 150))
    
    # Test parameters
    test_message = "Hello world! This is a test message with accents: áéíóú"
    test_password = "secret123"
    
    print(f"Original message: {test_message}")
    
    # Save test image
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, "test_input.png")
    output_path = os.path.join(temp_dir, "test_output.png")
    test_image.save(input_path)
    
    # Encode message
    print("Encoding message into image...")
    payload = steganography.build_payload_from_text(test_message, test_password)
    stego_image = steganography.embed_payload_into_image(test_image, payload)
    stego_image.save(output_path)
    
    # Decode message
    print("Decoding message from image...")
    decoded_payload = steganography.extract_payload_from_image(stego_image)
    decoded_message = steganography.extract_text_from_payload(decoded_payload, test_password)
    
    print(f"Decoded message: {decoded_message}")
    
    # Verify results
    if test_message == decoded_message:
        print("✅ Test passed: Original and decoded messages match!")
    else:
        print("❌ Test failed: Messages do not match!")
        print(f"Original: {test_message}")
        print(f"Decoded: {decoded_message}")
    
    # Clean up
    os.remove(input_path)
    os.remove(output_path)
    os.rmdir(temp_dir)

if __name__ == "__main__":
    test_end_to_end()
