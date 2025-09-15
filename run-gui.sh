#!/bin/bash

# Wrapper script to run ImageHide GUI with Xvfb if no display is available

if [ -z "$DISPLAY" ]; then
    echo "No DISPLAY set, running with Xvfb..."
    xvfb-run -a imagehide-gui
else
    echo "Using host display: $DISPLAY"
    imagehide-gui
fi
