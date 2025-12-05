# totp_utils.py
import base64
from typing import Tuple
import pyotp

def _validate_hex_seed(hex_seed: str) -> None:
    """Raise ValueError if seed is not a 64-character hex string."""
    if not isinstance(hex_seed, str):
        raise ValueError("hex_seed must be a string")
    s = hex_seed.strip().lower()
    if len(s) != 64:
        raise ValueError("hex_seed must be exactly 64 characters")
    try:
        bytes.fromhex(s)
    except ValueError:
        raise ValueError("hex_seed contains non-hex characters")

def _hex_to_base32(hex_seed: str) -> str:
    """Convert hex string -> bytes -> base32 (string)."""
    hex_seed = hex_seed.strip().lower()
    seed_bytes = bytes.fromhex(hex_seed)         # step: hex -> bytes
    b32 = base64.b32encode(seed_bytes).decode() # step: bytes -> base32 string
    return b32

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code from 64-char hex seed.
    Returns a 6-digit string (e.g., "123456").
    """
    _validate_hex_seed(hex_seed)
    b32_seed = _hex_to_base32(hex_seed)
    # Create TOTP (SHA-1, 30s, 6 digits)
    totp = pyotp.TOTP(b32_seed, digits=6, interval=30, digest='sha1')
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a 6-digit TOTP code with a ±valid_window tolerance.
    valid_window=1 accepts current period ±1 (i.e., ±30 seconds).
    Returns True if code is valid, False otherwise.
    """
    _validate_hex_seed(hex_seed)
    if not isinstance(code, str) or not code.isdigit() or len(code) != 6:
        return False
    b32_seed = _hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32_seed, digits=6, interval=30, digest='sha1')
    # verify returns True/False; valid_window provides tolerance
    return bool(totp.verify(code, valid_window=valid_window))
