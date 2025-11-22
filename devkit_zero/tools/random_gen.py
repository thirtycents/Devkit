"""
Random Data Generation Tool

Features: Generate UUIDs, passwords, random numbers, etc.
Owner: Unassigned
Priority: High
"""

# TODO: Implement random data generation functionality
# Refer to formatter.py structure for implementation

import random
import string
import uuid
import secrets
from typing import Optional


def generate_uuid(version: int = 4) -> str:
    """
    Generate UUID

    Args:
        version: UUID version (1, 4)

    Returns:
        UUID string
    """
    if version == 1:
        return str(uuid.uuid1())
    elif version == 4:
        return str(uuid.uuid4())
    else:
        raise ValueError(f"Unsupported UUID version: {version}")


def generate_random_string(length: int = 8,
                           include_numbers: bool = True,
                           include_uppercase: bool = True,
                           include_lowercase: bool = True,
                           include_symbols: bool = False,
                           custom_chars: Optional[str] = None) -> str:
    """
    Generate random string

    Args:
        length: String length
        include_numbers: Include numbers
        include_uppercase: Include uppercase letters
        include_lowercase: Include lowercase letters
        include_symbols: Include special symbols
        custom_chars: Custom character set

    Returns:
        Random string
    """
    if custom_chars:
        chars = custom_chars
    else:
        chars = ""
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if not chars:
        raise ValueError("At least one character type must be selected")

    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_secure_password(length: int = 16) -> str:
    """
    Generate secure password

    Args:
        length: Password length

    Returns:
        Secure password string
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    # Ensure password contains all character types
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"

    # At least one character of each type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+")
    ]

    # Fill remaining length
    for _ in range(length - 4):
        password.append(secrets.choice(chars))

    # Shuffle
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def generate_random_number(min_val: int = 0, max_val: int = 100) -> int:
    """
    Generate random integer

    Args:
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Random integer
    """
    return secrets.randbelow(max_val - min_val + 1) + min_val


def generate_random_float(min_val: float = 0.0, max_val: float = 1.0, precision: int = 2) -> float:
    """
    Generate random float

    Args:
        min_val: Minimum value
        max_val: Maximum value
        precision: Decimal places

    Returns:
        Random float
    """
    random_float = random.uniform(min_val, max_val)
    return round(random_float, precision)


def generate_random_hex_color() -> str:
    """
    Generate random hex color code

    Returns:
        Color code (e.g. #FF5733)
    """
    return f"#{random.randint(0, 0xFFFFFF):06X}"


def register_parser(subparsers):
    """Register parser for random-gen command"""
    parser = subparsers.add_parser('random', help='Random data generation tool')

    subcommands = parser.add_subparsers(dest='type', help='Generation type')

    # UUID Generation
    uuid_parser = subcommands.add_parser('uuid', help='Generate UUID')
    uuid_parser.add_argument('--version', '-v', type=int, choices=[1, 4], default=4,
                             help='UUID version (default: 4)')

    # Random String Generation
    string_parser = subcommands.add_parser('string', help='Generate random string')
    string_parser.add_argument('--length', '-l', type=int, default=8, help='String length (default: 8)')
    string_parser.add_argument('--no-numbers', action='store_true', help='Exclude numbers')
    string_parser.add_argument('--no-uppercase', action='store_true', help='Exclude uppercase letters')
    string_parser.add_argument('--no-lowercase', action='store_true', help='Exclude lowercase letters')
    string_parser.add_argument('--symbols', action='store_true', help='Include special symbols')
    string_parser.add_argument('--custom', help='Custom character set')

    # Secure Password Generation
    password_parser = subcommands.add_parser('password', help='Generate secure password')
    password_parser.add_argument('--length', '-l', type=int, default=16, help='Password length (default: 16)')

    # Random Number Generation
    number_parser = subcommands.add_parser('number', help='Generate random number')
    number_parser.add_argument('--min', type=int, default=0, help='Minimum value (default: 0)')
    number_parser.add_argument('--max', type=int, default=100, help='Maximum value (default: 100)')
    number_parser.add_argument('--float', action='store_true', help='Generate float number')
    number_parser.add_argument('--precision', type=int, default=2, help='Float precision (default: 2)')

    # Color Code Generation
    color_parser = subcommands.add_parser('color', help='Generate random color code')

    parser.set_defaults(func=main)


def main(args):
    """Main function for random-gen tool"""
    try:
        if args.type == 'uuid':
            return generate_uuid(args.version)

        elif args.type == 'string':
            return generate_random_string(
                length=args.length,
                include_numbers=not args.no_numbers,
                include_uppercase=not args.no_uppercase,
                include_lowercase=not args.no_lowercase,
                include_symbols=args.symbols,
                custom_chars=args.custom
            )

        elif args.type == 'password':
            return generate_secure_password(args.length)

        elif args.type == 'number':
            if args.float:
                min_val = float(args.min)
                max_val = float(args.max)
                return str(generate_random_float(min_val, max_val, args.precision))
            else:
                return str(generate_random_number(args.min, args.max))

        elif args.type == 'color':
            return generate_random_hex_color()

        else:
            raise ValueError("Please select generation type: uuid, string, password, number, color")

    except Exception as e:
        raise RuntimeError(f"Generation failed: {e}")


if __name__ == "__main__":
    # For standalone testing
    print("UUID:", generate_uuid())
    print("Random String:", generate_random_string(12))
    print("Secure Password:", generate_secure_password(16))
    print("Random Number:", generate_random_number(1, 100))
    print("Color Code:", generate_random_hex_color())