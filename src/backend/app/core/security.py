from datetile import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.content import CryptContext
from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check a plaintext password against its stored bcrypt hash.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The stored bcrypt hash to compare against.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    extra_claims: dict[str, Any] | None = None 
) -> str:
    """
    Create a JWT access token.

    Args:
        subject (str): The subject (usually user ID) for the token.
        extra_claims (dict[str, Any], optional): Additional claims to include
        in the token.

    Returns:
        str: The generated JWT access token.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expires_minutes
    )
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)
    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decode a JWT access token.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        dict[str, Any] | None: The decoded claims if the token is valid,
        otherwise None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None
