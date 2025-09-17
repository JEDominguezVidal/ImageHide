FROM python:3.8-slim

# Install system dependencies for PyQt5
RUN apt-get update && apt-get install -y \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5core5a \
    libqt5dbus5 \
    libglib2.0-0 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libfreetype6 \
    libpng16-16 \
    libjpeg62-turbo \
    libtiff6 \
    libwebp7 \
    libopenjp2-7 \
    liblcms2-2 \
    libharfbuzz0b \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Make scripts executable
RUN chmod +x run-gui.sh entrypoint.sh

# Install Python dependencies and the package
RUN pip install --no-cache-dir .

# Create images directory with proper permissions before switching to non-root user
RUN mkdir -p /app/images && \
    chmod 755 /app/images

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app/images
USER appuser

# Set environment variables
ENV DISPLAY=:0

# Custom entrypoint that handles both CLI and GUI
ENTRYPOINT ["./entrypoint.sh"]

# Default command (can be overridden)
CMD ["--help"]
