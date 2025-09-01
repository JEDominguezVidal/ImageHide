# ImageHide

ImageHide is a command-line tool to hide text messages inside images using least-significant-bit (LSB) steganography. Messages are encoded in UTF-16, lightly rotated by a password-derived shift, then encrypted with AES (password-derived key). The intention is to make the implementation modular and easy to extend.
