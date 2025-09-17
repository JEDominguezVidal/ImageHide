# ImageHide: Secure Image Steganography

## Project Description
ImageHide is a Python application that allows you to hide secret messages within images using steganography. Messages are encrypted with a two-layer security system:
1. **Password-based rotation cipher**: Shifts letters based on password length
2. **AES-256 encryption**: Industry-standard encryption algorithm
3. **LSB steganography**: Embeds encrypted messages in image pixels

The application supports:
- Both grayscale and colour images
- Unicode messages with diacritics
- CLI interface for script-based usage
- GUI interface for user-friendly interaction

## Project Structure

### File Structure:
```
.
├── pyproject.toml                 # Project configuration and dependencies
├── README.md                      # This documentation file
└── imagehide/                     # Main package directory
    ├── __init__.py                # Package initialisation
    ├── cli.py                     # Command-line interface entry point
    ├── gui.py                     # Graphical user interface
    ├── assets/                    # Project assests
    │   └── ImageHide_logo.ico     # GUI logo
    ├── core/                      # Core implementation modules
    │   ├── __init__.py            # Core package initialisation
    │   ├── config.py              # Constants for core functionality
    │   ├── crypto.py              # AES encryption and key derivation
    │   ├── encoding.py            # Text processing and rotation cipher
    │   ├── errors.py              # Custom exception classes
    │   ├── image_io.py            # Image loading/saving and analysis
    │   └── steganography.py       # LSB embedding/extraction logic
    └── tests/                     # Test files
        ├── __init__.py            # Tests package initialisation
        ├── test_all.py            # All tests executed in sequence
        ├── test_crypto.py         # Cryptography unit tests
        ├── test_integration.py    # End-to-end workflow test
        └── test_steganography.py  # Steganography unit tests
```

### Folder Structure:
- `imagehide/`: Main package containing the CLI, GUI, and core modules
- `imagehide/assets/`: Contains all assets used in the project
- `imagehide/core/`: Contains all core application logic
- `imagehide/tests/`: Unit and integration tests

## Installation and Usage

### Dependencies:
ImageHide has the following dependencies:
- Pillow>=9.0.0
- cryptography>=40.0
- numpy>=1.24
- pytest>=7.0
- **PyQt5>=5.15** (for GUI functionality)

### Installation:
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

### Potential Installation Issues:
One known issue has been detected when installing the PyQt5 library:
1. Installation getting stuck on "Preparing Wheel metadata..." when trying to install PyQt5 can be fixed by updating pip to the latest version (25.0.1 at the time of writing this document):
```bash
python -m pip install --upgrade pip
```

### Command Examples:
```bash
# Encode message into image (with password) using CLI
imagehide encode input.png -m "Secret Message" -p password -o output.png

# Decode message from image using CLI
imagehide decode output.png -p password

# Launch the GUI
imagehide-gui
```

### CLI Arguments:
| Argument | Description | Example |
|----------|-------------|---------|
| `image` | Input image path (positional) | `input.png` |
| `-o`, `--output` | Output image path | `-o secret.png` |
| `-m`, `--message` | Message to hide | `-m "Top Secret"` |
| `-p`, `--password` | Password for encryption | `-p mypassword` |

## Docker Usage

ImageHide can be run in a Docker container without installing dependencies on the host system.

### Quick Setup

Before running ImageHide in Docker, run the setup script to prepare your environment:

```bash
# Run the setup script to prepare directories and permissions
./setup.sh
```

This will:
- Create `input/` and `output/` directories
- Fix directory permissions
- Copy a sample image for testing

### Building the Docker Image

```bash
# Build the Docker image
docker build -t imagehide .
```

### Running CLI Commands

```bash
# Encode message
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output imagehide encode /app/input/sample.png -m "Secret Message" -p password -o /app/output/output.png

# Decode message
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output imagehide decode /app/output/output.png -p password
```

### Running GUI

For GUI usage, you need to allow Docker to access your X server:

```bash
# Allow local connections to X server
xhost +local:docker

# Run GUI
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output imagehide /bin/bash -c "./run-gui.sh"

# Revoke X server access after use
xhost -local:docker
```

### Using Docker Compose

Create `input/` and `output/` directories in your project root, then:

```bash
# Build the image
docker-compose build

# Run CLI commands
docker-compose run --rm imagehide encode /app/input/sample.png -m "Secret Message" -p password -o /app/output/output.png
docker-compose run --rm imagehide decode /app/output/output.png -p password

# Run GUI
docker-compose run --rm imagehide /bin/bash -c "./run-gui.sh"
```

**Note**: Docker Compose now uses your host user ID to avoid permission issues. If you encounter permission problems, you can set the UID and GID environment variables:

```bash
export UID=$(id -u)
export GID=$(id -g)
docker-compose run --rm imagehide encode /app/input/input.png -m "Secret Message" -p password -o /app/output/output.png
```

### Notes:
- Mount your input/output directories as volumes
- For GUI, ensure X11 forwarding is properly configured
- The container includes Xvfb for headless GUI operation if DISPLAY is not set
