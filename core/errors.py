# Custom exceptions for ImageHide application

class ImageHideError(Exception):
    """Base class for all ImageHide-specific errors."""
    pass

class CapacityError(ImageHideError):
    """Raised when an image lacks sufficient capacity for a payload."""
    def __init__(self, required_bits, available_bits):
        self.required_bits = required_bits
        self.available_bits = available_bits
        super().__init__(
            f"Payload requires {required_bits} bits of capacity "
            f"but image only has {available_bits} bits available"
        )

class FormatError(ImageHideError):
    """Raised when encountering invalid data formats."""
    def __init__(self, message="Invalid data format", details=None):
        self.details = details
        if details:
            super().__init__(f"{message}: {details}")
        else:
            super().__init__(message)

class DecryptionError(ImageHideError):
    """Raised when decryption fails due to incorrect key or corrupted data."""
    def __init__(self, message="Decryption failed - invalid key or corrupted data", cause=None):
        self.cause = cause
        if cause:
            super().__init__(f"{message}: {str(cause)}")
        else:
            super().__init__(message)
