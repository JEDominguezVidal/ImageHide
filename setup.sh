#!/bin/bash

# ImageHide Docker Setup Script
# This script prepares the environment for running ImageHide in Docker

echo "🚀 Setting up ImageHide Docker environment..."

# Create images directory if it doesn't exist
if [ ! -d "images" ]; then
    echo "📁 Creating images directory..."
    mkdir -p images
fi

# Fix permissions for the directory
echo "🔧 Fixing directory permissions..."
chmod 755 images/

# Check if there's a sample image to copy
if [ -f "imagehide/assets/sample.png" ]; then
    echo "📋 Copying sample image to images directory..."
    cp imagehide/assets/sample.png images/sample.png
    echo "✅ Sample image copied to images/sample.png"
elif [ -f "imagehide/assets/ImageHide_logo.png" ]; then
    echo "📋 Copying logo image to images directory..."
    cp imagehide/assets/ImageHide_logo.png images/sample.png
    echo "✅ Sample image copied to images/sample.png"
else
    echo "⚠️  No sample image found. You'll need to add your own image to the images/ directory."
fi

echo "✅ Setup complete!"
echo ""
echo "📖 Usage examples:"
echo "  # CLI encoding (unified with GUI behavior):"
echo "  docker run --rm -v \$(pwd)/images:/app/images imagehide encode /app/images/sample.png -m 'Secret Message' -p password"
echo "  # This creates: images/sample_steganography.png"
echo ""
echo "  # CLI decoding:"
echo "  docker run --rm -v \$(pwd)/images:/app/images imagehide decode /app/images/sample_steganography.png -p password"
echo ""
echo "  # GUI (requires X11):"
echo "  xhost +local:docker"
echo "  docker run --rm -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v \$(pwd)/images:/app/images imagehide /bin/bash -c './run-gui.sh'"
