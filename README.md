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
- Docker container execution for dependency-free deployment

## Project Structure

### File Structure:
```
.
├── pyproject.toml                 # Project configuration and dependencies
├── README.md                      # This documentation file
├── scripts/                       # Docker and setup scripts
│   ├── setup.sh                   # Docker environment setup script
│   ├── run-gui.sh                 # GUI launcher script
│   └── entrypoint.sh              # Docker entrypoint script
├── Dockerfile                     # Docker container configuration
├── docker-compose.yml             # Docker Compose configuration
└── imagehide/                     # Main package directory
    ├── __init__.py                # Package initialisation
    ├── cli.py                     # Command-line interface entry point
    ├── gui.py                     # Graphical user interface
    ├── assets/                    # Project assets
    │   ├── ImageHide_logo.ico     # GUI logo
    │   └── sample.png             # Sample image for testing
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
- `scripts/`: Contains Docker and setup scripts for containerized execution
- `imagehide/`: Main package containing the CLI, GUI, and core modules
- `imagehide/assets/`: Contains all assets used in the project
- `imagehide/core/`: Contains all core application logic
- `imagehide/tests/`: Unit and integration tests

## Installation and Usage (CLI/GUI)

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

### Usage Examples:

#### CLI Usage:
```bash
# Encode message into image (with password)
imagehide encode input.png -m "Secret Message" -p password -o output.png

# Decode message from image
imagehide decode output.png -p password
```

#### GUI Usage:
```bash
# Launch the graphical interface
imagehide-gui
```

### CLI Arguments:
| Argument | Description | Example |
|----------|-------------|---------|
| `image` | Input image path (positional) | `input.png` |
| `-o`, `--output` | Output image path | `-o secret.png` |
| `-m`, `--message` | Message to hide | `-m "Top Secret"` |
| `-p`, `--password` | Password for encryption | `-p mypassword` |

## Installation and Usage (Docker)

### Dependencies:
ImageHide has the following dependencies (automatically handled in Docker):
- Pillow>=9.0.0
- cryptography>=40.0
- numpy>=1.24
- pytest>=7.0
- **PyQt5>=5.15** (for GUI functionality)

### Installation:
No installation required on the host system. Simply ensure Docker is installed and run:

```bash
# Clone the repository
git clone https://github.com/JEDominguezVidal/ImageHide.git
cd ImageHide

# Run setup script
./scripts/setup.sh

# Build Docker image
docker build -t imagehide .
```

### Potential Installation Issues:
1. **Docker not installed**: Install Docker following the [official documentation](https://docs.docker.com/get-docker/)
2. **Permission issues**: You may need to run Docker commands with `sudo` or add your user to the `docker` group
3. **X11 forwarding for GUI**: Ensure X11 is properly configured on your system for GUI usage

### Docker Usage

ImageHide can be run in a Docker container without installing dependencies on the host system.

#### Quick Setup

Before running ImageHide in Docker, run the setup script to prepare your environment:

```bash
# Run the setup script to prepare directories and permissions
./scripts/setup.sh
```

This will:
- Create `images/` directory
- Fix directory permissions
- Copy a sample image for testing

#### Building the Docker Image

```bash
# Build the Docker image
docker build -t imagehide .
```

#### Running CLI Commands

**Unified behavior**: CLI and GUI now work identically - both read from and write to the same directory, using "_steganography" suffix for output files.

```bash
# Encode message (creates sample_steganography.png in images/)
docker run --rm -v $(pwd)/images:/app/images imagehide encode /app/images/sample.png -m "Secret Message" -p password

# Decode message
docker run --rm -v $(pwd)/images:/app/images imagehide decode /app/images/sample_steganography.png -p password
```

#### Running GUI

For GUI usage, you need to allow Docker to access your X server:

```bash
# Allow local connections to X server
xhost +local:docker

# Run GUI
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd)/images:/app/images imagehide /bin/bash -c "./scripts/run-gui.sh"

# Revoke X server access after use
xhost -local:docker
```

### Using Docker Compose

```bash
# Build the image
docker-compose build

# Run CLI commands (unified with GUI behavior)
docker-compose run --rm imagehide encode /app/images/sample.png -m "Secret Message" -p password
docker-compose run --rm imagehide decode /app/images/sample_steganography.png -p password

# Run GUI
docker-compose run --rm imagehide /bin/bash -c "./scripts/run-gui.sh"
```

**Note**: Docker Compose now uses your host user ID to avoid permission issues. If you encounter permission problems, you can set the UID and GID environment variables:

```bash
export UID=$(id -u)
export GID=$(id -g)
docker-compose run --rm imagehide encode /app/images/sample.png -m "Secret Message" -p password
```

#### Notes:
- Mount your "images/" directory as a volume
- For GUI, ensure X11 forwarding is properly configured
- The container includes Xvfb for headless GUI operation if DISPLAY is not set
