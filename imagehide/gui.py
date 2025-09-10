"""Graphical User Interface for ImageHide.

This module implements a Qt-based GUI for the ImageHide application, providing
a user-friendly interface to encode and decode messages in images using
steganography techniques. The interface includes file selection, password
protection, and message handling components.
"""

import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from imagehide.core import image_io, steganography, errors


class ImageHideGUI(QMainWindow):
    """Main application window for the ImageHide GUI.

    This class sets up the user interface and handles all user interactions
    for encoding and decoding messages in images.
    """

    def __init__(self) -> None:
        """Initialise the main window and set up the UI components."""
        super().__init__()
        self.setWindowTitle("ImageHide Steganography")
        self.setGeometry(100, 100, 600, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Input Image section
        image_layout = QHBoxLayout()
        layout.addLayout(image_layout)
        
        image_layout.addWidget(QLabel("Input Image:"))
        self.image_path = QLineEdit()
        self.image_path.setReadOnly(True)
        image_layout.addWidget(self.image_path)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_image)
        image_layout.addWidget(browse_btn)
        
        # Password section
        password_layout = QHBoxLayout()
        layout.addLayout(password_layout)
        
        password_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)
        
        # Message section
        message_layout = QVBoxLayout()
        layout.addLayout(message_layout)
        
        message_layout.addWidget(QLabel("Message:"))
        self.message_input = QTextEdit()
        message_layout.addWidget(self.message_input)
        
        # Action buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        self.encode_btn = QPushButton("Encode")
        self.encode_btn.clicked.connect(self.encode_message)
        button_layout.addWidget(self.encode_btn)
        
        self.decode_btn = QPushButton("Decode")
        self.decode_btn.clicked.connect(self.decode_message)
        button_layout.addWidget(self.decode_btn)
        
        # Status display
        status_layout = QVBoxLayout()
        layout.addLayout(status_layout)
        
        status_layout.addWidget(QLabel("Status:"))
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        status_layout.addWidget(self.status_display)
    
    def browse_image(self) -> None:
        """Open a file dialog to select an image file.
        
        Sets the selected file path to the image path field.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.image_path.setText(file_path)
    
    def encode_message(self) -> None:
        """Encode a message into the selected image.
        
        Validates input fields, builds and embeds the payload, then saves
        the steganographed image with '_steganography.png' suffix.
        
        Shows success message or error in the status display.
        """
        image_path = self.image_path.text()
        password = self.password_input.text()
        message = self.message_input.toPlainText()
        
        if not all([image_path, password, message]):
            self.show_error("All fields are required for encoding")
            return
        
        try:
            # Load image
            image = image_io.load_image(image_path)
            
            # Build and embed payload
            payload = steganography.build_payload_from_text(message, password)
            stego_image = steganography.embed_payload_into_image(image, payload)
            
            # Generate output path
            base, _ = os.path.splitext(image_path)
            output_path = f"{base}_steganography.png"
            
            # Save output
            image_io.save_image(stego_image, output_path)
            timestamp = self._format_timestamp()
            self.status_display.append(f"[{timestamp}] Message embedded successfully in {output_path}")
        except Exception as e:
            self.show_error(str(e))
    
    def decode_message(self) -> None:
        """Decode a message from the selected image.
        
        Validates input fields, extracts the payload, decrypts the message,
        and populates the message field with the decoded text.
        
        Shows success message or error in the status display.
        """
        image_path = self.image_path.text()
        password = self.password_input.text()
        
        if not all([image_path, password]):
            self.show_error("Image path and password are required for decoding")
            return
        
        try:
            # Load image
            image = image_io.load_image(image_path)
            
            # Extract payload and text
            payload = steganography.extract_payload_from_image(image)
            message = steganography.extract_text_from_payload(payload, password)
            
            # Update message field
            self.message_input.setPlainText(message)
            timestamp = self._format_timestamp()
            self.status_display.append(f"[{timestamp}] Message decoded successfully")
        except Exception as e:
            self.show_error(str(e))
    
    def _format_timestamp(self) -> str:
        """Return current timestamp in 'YYYY-MM-DD HH:MM:SS' format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def show_error(self, message) -> None:
        """Display an error message in a dialog and the status display.
        
        Args:
            message: The error message to display
        """
        QMessageBox.critical(self, "Error", message)
        timestamp = self._format_timestamp()
        self.status_display.append(f"[{timestamp}] Error: {message}")


def main() -> None:
    """Entry point for the GUI application.
    
    Initialises the QApplication and main window, then starts the event loop.
    """
    app = QApplication(sys.argv)
    window = ImageHideGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
