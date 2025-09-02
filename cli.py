# Command-line interface for ImageHide.
#
# This module implements the user-facing CLI surface for the ImageHide
# application. It defines argument parsing, validation and top-level
# orchestration for 'encode' and 'decode' commands.

import argparse
import os
import sys
import getpass
from typing import Optional, List
from core import image_io, steganography, errors
from core.errors import CapacityError, FormatError, DecryptionError

def main(argv: Optional[List[str]] = None) -> None:
    """Primary CLI entry point."""
    args = parse_args(argv)
    try:
        if args.command == 'encode':
            validate_args_for_encode(args)
            encode_command(
                image_path=args.image,
                message=args.message,
                password=args.password,
                output_path=args.output
            )
        elif args.command == 'decode':
            validate_args_for_decode(args)
            result = decode_command(
                image_path=args.image,
                password=args.password
            )
            print(f"Decoded message: {result}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Construct and parse the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="imagehide",
        description="ImageHide: Hide messages in images using steganography"
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode a message into an image')
    # encode_parser.add_argument('image', help='Path to input image')
    encode_parser.add_argument('-i', '--image', help='Path to input image')
    encode_parser.add_argument('-m', '--message', help='Message to hide (use - for stdin)', default='')
    encode_parser.add_argument('-p', '--password', help='Password to protect the message', required=True)
    encode_parser.add_argument('-o', '--output', help='Output image path', default=None)
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode a message from an image')
    # decode_parser.add_argument('image', help='Path to image containing hidden message')
    decode_parser.add_argument('-i', '--image', help='Path to image containing hidden message')
    decode_parser.add_argument('-p', '--password', help='Password to decrypt the message', required=True)

    return parser.parse_args(argv)

def validate_args_for_encode(args: argparse.Namespace) -> None:
    """Validate arguments provided to the 'encode' subcommand."""
    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Input image not found: {args.image}")
    
    if args.message == '':
        raise ValueError("Message cannot be empty")
    elif args.message == '-':
        args.message = sys.stdin.read().strip()
    
    if args.output and os.path.exists(args.output):
        print(f"Warning: Output file {args.output} will be overwritten", file=sys.stderr)

def validate_args_for_decode(args: argparse.Namespace) -> None:
    """Validate arguments provided to the 'decode' subcommand."""
    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Input image not found: {args.image}")

def encode_command(image_path: str, message: str, password: str, output_path: Optional[str] = None) -> None:
    """High-level encode operation."""
    # Load image
    image = image_io.load_image(image_path)
    
    # Build payload
    payload = steganography.build_payload_from_text(message, password)
    
    # Check capacity
    required_bits = steganography.calculate_required_bits_for_payload(len(payload))
    available_bits = image_io.get_capacity_bits(image)
    if required_bits > available_bits:
        raise CapacityError(
            f"Message too large for image. Required: {required_bits} bits, "
            f"Available: {available_bits} bits"
        )
    
    # Embed payload
    stego_image = steganography.embed_payload_into_image(image, payload)
    
    # Save output
    if not output_path:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_stego{ext}"
    
    image_io.save_image(stego_image, output_path)
    print(f"Message embedded successfully in {output_path}")

def decode_command(image_path: str, password: str) -> str:
    """High-level decode operation which extracts and returns the message."""
    # Load image
    image = image_io.load_image(image_path)
    
    # Extract payload
    payload = steganography.extract_payload_from_image(image)
    
    # Extract text
    return steganography.extract_text_from_payload(payload, password)

def prompt_password(confirm: bool = False) -> str:
    """Securely prompt the user for a password."""
    password = getpass.getpass("Enter password: ")
    if confirm:
        confirm_pw = getpass.getpass("Confirm password: ")
        if password != confirm_pw:
            raise ValueError("Passwords do not match")
    return password

if __name__ == "__main__":
    main()