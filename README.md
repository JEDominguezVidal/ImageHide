# ImageHide: Secure Image Steganography

## Project Description
ImageHide is a Python application that allows you to hide secret messages within images using steganography. Messages are encrypted with a two-layer security system:
1. **Password-based rotation cipher**: Shifts letters based on password length
2. **AES-256 encryption**: Industry-standard encryption algorithm
3. **LSB steganography**: Embeds encrypted messages in image pixels

The application supports:
- Both grayscale and color images
- Unicode messages with diacritics
- CLI interface for easy integration

## Project Structure

### File Structure
```
.
├── cli.py                     # Command-line interface
├── README.md                  # This documentation file
├── requirements.txt           # Python dependencies
└── core/                      # Main implementation modules
    ├── steganography.py       # LSB embedding/extraction logic
    ├── crypto.py              # AES encryption and key derivation
    ├── encoding.py            # Text processing and rotation cipher
    ├── image_io.py            # Image loading/saving and analysis
    └── errors.py              # Custom exception classes
└── tests/                     # Test files to check funtionalities
    ├── test_crypto.py         # Cryptography unit tests
    ├── test_steganography.py  # Steganography unit tests
    ├── test_integration.py    # End-to-end workflow test
    └── test_all.py            # All tests executed in sequence
```

### Folder Structure
- `core/`: Contains all core application logic
- `scripts/`: Contains executable scripts (currently empty)
- `tests/`: Unit and integration tests

## Usage

### Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### Command Examples
```bash
# Encode message into image (with password)
python cli.py encode -i input.png -m "Secret Message" -p password -o output.png

# Decode message from image
python cli.py decode -i output.png -p password
```

### Arguments
| Argument | Description | Example |
|----------|-------------|---------|
| `-i`, `--input` | Input image path | `-i photo.png` |
| `-o`, `--output` | Output image path | `-o secret.png` |
| `-m`, `--message` | Message to hide | `-m "Top Secret"` |
| `-p`, `--password` | Password for encryption | `-p mypassword` |
