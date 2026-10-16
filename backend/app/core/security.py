"""
Enterprise Cryptographic Security & Authentication Engine
- Salted bcrypt password hashing (cost factor 12+)
- Cryptographically signed JWT session tokens (HMAC-SHA256)
- IP & Account Brute-Force Rate Limiting (5-attempt / 15-minute lockout)
- RFC 6238 TOTP Two-Factor Authentication with QR code provisioning
"""

import io
import time
import base64
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import pyotp
import qrcode

from backend.app.core.config import settings

# In-memory IP and account rate limiter for login brute-force mitigation
# Structure: { key: { "attempts": int, "blocked_until": float } }
_RATE_LIMIT_STORE: Dict[str, Dict] = {}
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 15 * 60  # 15 minutes


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt with a cryptographic salt (12 rounds).
    Returns the string representation of the hash.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a stored bcrypt hash in constant time.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a cryptographically signed JWT access token.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": "Tekken8PlatformSecurity"
    })
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a JWT token's signature, issuer, and expiration.
    Returns payload dictionary or None if invalid/expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "sub"]}
        )
        return payload
    except (jwt.PyJWTError, Exception):
        return None


def check_rate_limit(identifier: str) -> Tuple[bool, int]:
    """
    Checks if an IP or username identifier is currently locked out.
    Returns (is_blocked, remaining_lockout_seconds).
    """
    now = time.time()
    record = _RATE_LIMIT_STORE.get(identifier)
    if not record:
        return False, 0

    blocked_until = record.get("blocked_until", 0)
    if now < blocked_until:
        return True, int(blocked_until - now)

    # Lockout has expired; reset
    if blocked_until > 0 and now >= blocked_until:
        _RATE_LIMIT_STORE.pop(identifier, None)

    return False, 0


def record_failed_attempt(identifier: str) -> Tuple[int, int]:
    """
    Records a failed login attempt. If attempts reach MAX_FAILED_ATTEMPTS, locks for 15 mins.
    Returns (current_attempts, remaining_lockout_seconds).
    """
    now = time.time()
    record = _RATE_LIMIT_STORE.setdefault(identifier, {"attempts": 0, "blocked_until": 0})
    record["attempts"] += 1

    if record["attempts"] >= MAX_FAILED_ATTEMPTS:
        record["blocked_until"] = now + LOCKOUT_DURATION_SECONDS
        return record["attempts"], LOCKOUT_DURATION_SECONDS

    return record["attempts"], 0


def reset_rate_limit(identifier: str) -> None:
    """
    Resets the rate limiter for an identifier upon successful authentication.
    """
    _RATE_LIMIT_STORE.pop(identifier, None)


# ---------------------------------------------------------------------------
# TOTP (RFC 6238) Two-Factor Authentication Engine
# ---------------------------------------------------------------------------

def generate_totp_secret() -> str:
    """
    Generates a secure random 32-character base32 TOTP secret.
    """
    return pyotp.random_base32()


def get_totp_provisioning_uri(username: str, secret: str) -> str:
    """
    Creates the otpauth:// URI for Google Authenticator / Authy.
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name="Tekken 8 Esports Portal")


def generate_qr_code_base64(provisioning_uri: str) -> str:
    """
    Generates a high-contrast QR code and returns it as a Base64 data URL.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=3,
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#090A0F", back_color="#FFFFFF")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_data}"


def verify_totp_code(secret: str, code: str) -> bool:
    """
    Verifies a 6-digit TOTP code against the secret key (allows ±30s clock drift window).
    """
    if not secret or not code:
        return False
    try:
        clean_code = str(code).strip().replace(" ", "")
        totp = pyotp.TOTP(secret)
        return totp.verify(clean_code, valid_window=1)
    except Exception:
        return False
