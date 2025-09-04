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
├── pyproject.toml            # Project configuration and dependencies
├── README.md                 # This documentation file
└── imagehide/                # Main package directory
    ├── __init__.py           # Package initialization
    ├── cli.py                # Command-line interface entry point
    ├── config.py             # Configuration settings
    ├── core/                 # Core implementation modules
    │   ├── __init__.py       # Core package initialization
    │   ├── crypto.py         # AES encryption and key derivation
    │   ├── encoding.py       # Text processing and rotation cipher
    │   ├── errors.py         # Custom exception classes
    │   ├── image_io.py       # Image loading/saving and analysis
    │   ├── steganography.py  # LSB embedding/extraction logic
    └── tests/                    # Test files
        ├── __init__.py           # Tests package initialization
        ├── test_all.py           # All tests executed in sequence
        ├── test_crypto.py        # Cryptography unit tests
        ├── test_integration.py   # End-to-end workflow test
        └── test_steganography.py # Steganography unit tests
```

### Folder Structure
- `imagehide/`: Main package containing the CLI and core modules
- `imagehide/core/`: Contains all core application logic
- `imagehide/tests/`: Unit and integration tests

## Usage

### Dependencies
ImageHide has the following dependencies:
- Pillow>=9.0.0
- cryptography>=40.0
- numpy>=1.24
- pytest>=7.0

### Installation
ImageHide can be installed as a standard Linux application using pip:

```bash
# Download this repository
git clone https://github.com/JEDominguezVidal/ImageHide.git

# Install the package and dependencies
cd ImageHide
pip install .

# Verify installation
imagehide --help
```

### Command Examples
```bash
# Encode message into image (with password)
imagehide encode input.png -m "Secret Message" -p password -o output.png

# Decode message from image
imagehide decode output.png -p password
```

### Arguments
| Argument | Description | Example |
|----------|-------------|---------|
| `image` | Input image path (positional) | `input.png` |
| `-o`, `--output` | Output image path | `-o secret.png` |
| `-m`, `--message` | Message to hide | `-m "Top Secret"` |
| `-p`, `--password` | Password for encryption | `-p mypassword` |
