"""Security module for authentication and authorization.

Provides password hashing (Bcrypt) and JWT token creation/verification
functionality.
"""

from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt

from app.modules.core.config import settings


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password string.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash.

    Args:
        plain_password: The plaintext password to check.
        hashed_password: The hashed password to verify against.

    Returns:
        True if the password matches, False otherwise.
    """
    pwd_bytes = plain_password.encode("utf-8")
    hashed_pwd_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_pwd_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a new JWT access token.

    Args:
        data: The payload data to encode in the token.
        expires_delta: Optional expiration time delta. Defaults to 15 minutes.

    Returns:
        The encoded JWT token string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """Verify and decode a JWT access token.

    Args:
        token: The JWT token string to verify.

    Returns:
        The decoded payload if verification succeeds, None otherwise.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
