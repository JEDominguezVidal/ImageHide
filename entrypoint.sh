#!/bin/bash

# Custom entrypoint script for ImageHide Docker container
# This allows both CLI and GUI execution

# If the first argument is a shell command, execute it
if [[ "$1" == "/bin/bash" ]] || [[ "$1" == "bash" ]] || [[ "$1" == "sh" ]]; then
    exec "$@"
fi

# Otherwise, run imagehide with the provided arguments
exec imagehide "$@"
