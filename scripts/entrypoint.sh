#!/bin/bash

# Custom entrypoint script for ImageHide Docker container
# This allows both CLI and GUI execution

# Fix permissions for mounted volumes if they exist
echo "🔧 Fixing permissions for mounted volumes..."
if [ -d "/app/images" ]; then
    chmod 755 /app/images 2>/dev/null || echo "⚠️  Could not fix images directory permissions"
    # Try to change ownership if running as root
    if [ "$(id -u)" = "0" ]; then
        chown appuser:appuser /app/images 2>/dev/null || true
    fi
fi

# If the first argument is a shell command, execute it
if [[ "$1" == "/bin/bash" ]] || [[ "$1" == "bash" ]] || [[ "$1" == "sh" ]]; then
    exec "$@"
fi

# Otherwise, run imagehide with the provided arguments
exec imagehide "$@"
