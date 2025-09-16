#!/bin/bash

# ImageHide Docker Setup Script
# This script prepares the environment for running ImageHide in Docker

echo "🚀 Setting up ImageHide Docker environment..."

# Create input and output directories if they don't exist
if [ ! -d "input" ]; then
    echo "📁 Creating input directory..."
    mkdir -p input
fi

if [ ! -d "output" ]; then
    echo "📁 Creating output directory..."
    mkdir -p output
fi

# Fix permissions for the directories
echo "🔧 Fixing directory permissions..."
chmod 755 input/
chmod 755 output/

# Check if there's a sample image to copy
if [ -f "imagehide/assets/test.png" ]; then
    echo "📋 Copying sample image to input directory..."
    cp imagehide/assets/test.png input/sample.png
    echo "✅ Sample image copied to input/sample.png"
elif [ -f "imagehide/assets/ImageHide_logo.png" ]; then
    echo "📋 Copying logo image to input directory..."
    cp imagehide/assets/ImageHide_logo.png input/sample.png
    echo "✅ Sample image copied to input/sample.png"
else
    echo "⚠️  No sample image found. You'll need to add your own image to the input/ directory."
fi

echo "✅ Setup complete!"
echo ""
echo "📖 Usage examples:"
echo "  # CLI encoding:"
echo "  docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output imagehide encode /app/input/sample.png -m 'Secret Message' -p password -o /app/output/output.png"
echo ""
echo "  # CLI decoding:"
echo "  docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output imagehide decode /app/output/output.png -p password"
echo ""
echo "  # GUI (requires X11):"
echo "  xhost +local:docker"
echo "  docker run --rm -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output imagehide /bin/bash -c './run-gui.sh'"
