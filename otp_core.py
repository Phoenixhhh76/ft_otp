"""Core OTP helpers.

This file contains the parts that are worth learning first:
- reading and validating the hex key
- turning time into a moving counter
- generating HOTP/TOTP with HMAC-SHA1
"""

from __future__ import annotations

import hmac
import re
import struct
import time
from hashlib import sha1

from errors import ValidationError


HEX_KEY_RE = re.compile(r"^[0-9a-fA-F]{64,}$")


def normalize_hex_key(raw_text: str) -> str:
    """Remove surrounding whitespace and reject invalid key content."""

    candidate = raw_text.strip()
    if not HEX_KEY_RE.fullmatch(candidate):
        raise ValidationError("key must be 64 hexadecimal characters.")
    return candidate.lower()


def read_hex_key_file(path: str) -> bytes:
    """Read a key file, validate it, and convert it from hex to bytes."""

    with open(path, "r", encoding="utf-8") as handle:
        raw_text = handle.read()

    normalized = normalize_hex_key(raw_text)
    return bytes.fromhex(normalized)


def counter_from_time(timestamp: int | None = None, period: int = 30) -> int:
    """Convert unix time into the moving TOTP counter."""

    if period <= 0:
        raise ValidationError("period must be greater than zero.")

    current_time = int(time.time()) if timestamp is None else int(timestamp)
    return current_time // period


def hotp(secret: bytes, counter: int, digits: int = 6) -> str:
    """Generate a 6-digit HOTP code following RFC 4226."""

    if counter < 0:
        raise ValidationError("counter cannot be negative.")
    if digits <= 0:
        raise ValidationError("digits must be greater than zero.")

    counter_bytes = struct.pack(">Q", counter)
    digest = hmac.new(secret, counter_bytes, sha1).digest()

    offset = digest[-1] & 0x0F
    binary_code = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    otp_value = binary_code % (10**digits)

    return str(otp_value).zfill(digits)


def totp(
    secret: bytes,
    timestamp: int | None = None,
    period: int = 30,
    digits: int = 6,
) -> str:
    """Generate a TOTP code by reusing the HOTP algorithm."""

    counter = counter_from_time(timestamp=timestamp, period=period)
    return hotp(secret=secret, counter=counter, digits=digits)
