from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from fastapi import Response
from jose import JWTError, jwt

from app.core import SecurityConfig, settings


def set_app_cookie(
    response: Response, cookie_name: str, cookie_value: Any, expiry: int = 900
) -> None:
    """
    Set an application cookie on the given HTTP response with appropriate security settings.

    Args:
        response (Response): The FastAPI Response object to set the cookie on.
        cookie_name (str): The name of the cookie.
        cookie_value (Any): The value to assign to the cookie.
        expiry (int, optional): The max age of the cookie in seconds. Defaults to 900 (15 minutes).

    Behavior:
        - Applies secure and httponly flags if running in production mode.
        - Sets SameSite to "none" for production, "lax" otherwise.
    """
    is_production = settings.APP_ENV == "production"
    response.set_cookie(
        key=cookie_name,
        value=cookie_value,
        httponly=is_production,
        secure=is_production,
        samesite="none" if is_production else "lax",
        max_age=expiry,
    )


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Args:
        password (str): The plaintext password.
    Returns:
        str: The bcrypt hash of the password.
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against the stored bcrypt hash.
    Args:
        plain_password (str): The input password.
        hashed_password (str): The bcrypt hash from the database.
    Returns:
        bool: True if passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_jwt_token(
    data: dict,
    expires_delta: timedelta | None = None,
    secret_key: str | None = None,
    algorithm: str | None = None,
) -> str:
    """
    Create a JWT access or refresh token.
    Args:
        data: Data to encode in the token.
        expires_delta: Expiry duration; if None, use default.
        secret_key: Override secret key; uses settings otherwise.
        algorithm: Override algorithm; uses settings otherwise.
    Returns:
        JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    key = secret_key or SecurityConfig.SECRET_KEY
    alg = algorithm or SecurityConfig.ALGORITHM
    encoded_jwt = jwt.encode(to_encode, key, algorithm=alg)
    return encoded_jwt


def decode_jwt_token(
    token: str, secret_key: str | None = None, algorithms: list[str] | None = None
) -> dict[str, Any]:
    """
    Decode a JWT token and return its payload.
    Args:
        token: The JWT token string.
        secret_key: Secret key for verifying (defaults to settings).
        algorithms: Allowed algorithms (defaults to settings).
    Returns:
        The decoded payload dict.
    Raises:
        jose.JWTError if invalid.
    """
    key = secret_key or SecurityConfig.SECRET_KEY
    allowed_algorithms = algorithms or [SecurityConfig.ALGORITHM]
    try:
        payload = jwt.decode(token, key, algorithms=allowed_algorithms)
        return payload
    except JWTError:
        raise


def create_access_token(subject: str, extra_data: dict = None) -> str:
    """
    Create an access token (short-lived) for a subject (user id/email).
    Args:
        subject: The subject claim (e.g., user id).
        extra_data: Additional claims (optional).
    Returns:
        JWT string.
    """
    to_encode = {"sub": subject}
    if extra_data:
        to_encode.update(extra_data)
    expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_jwt_token(to_encode, expires_delta=expires)


def create_refresh_token(subject: str, extra_data: dict = None) -> str:
    """
    Create a refresh token (long-lived) for a subject.
    Args:
        subject: The subject claim (e.g., user id).
        extra_data: Additional claims (optional).
    Returns:
        JWT string.
    """
    to_encode = {"sub": subject}
    if extra_data:
        to_encode.update(extra_data)
    expires = timedelta(minutes=SecurityConfig.REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_jwt_token(to_encode, expires_delta=expires, secret_key=SecurityConfig.REFRESH_KEY)


def verify_jwt_token(token: str, refresh: bool = False) -> dict[str, Any]:
    """
    Verify and decode a JWT access/refresh token.
    Args:
        token: The JWT token string.
        refresh: If True, uses refresh secret and expiry config.
    Returns:
        Decoded payload.
    Raises:
        jose.JWTError if invalid or expired.
    """
    key = SecurityConfig.REFRESH_KEY if refresh else SecurityConfig.SECRET_KEY
    try:
        payload = jwt.decode(token, key, algorithms=[SecurityConfig.ALGORITHM])
        return payload
    except JWTError:
        raise
