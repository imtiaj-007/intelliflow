from functools import lru_cache
from typing import Any, Dict, List

from app.core.settings import settings


class SecurityConfig:
    """
    Security configuration class that handles authentication and authorization settings.

    This class centralizes all security-related configurations including API keys,
    secret keys, JWT algorithm, and token expiration settings. All values are
    sourced from the application settings with appropriate fallback defaults.

    Attributes:
        API_KEY (str): API key for authentication, sourced from application settings
        SECRET_KEY (str): Secret key for cryptographic operations, sourced from application settings
        ALGORITHM (str): JWT algorithm used for token encoding/decoding (default: HS256)
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Access token expiration time in minutes, sourced from settings with fallback
        REFRESH_TOKEN_EXPIRE_DAYS (int): Refresh token expiration time in days (default: 7)
        CORS_ORIGINS (list): List of allowed CORS origins including frontend base URL
        SECURITY_HEADERS (dict): Dictionary of security headers for HTTP responses
        RATE_LIMIT_REQUESTS (int): Maximum number of requests allowed in rate limit window
        RATE_LIMIT_WINDOW (int): Rate limit window duration in seconds (default: 900 = 15 minutes)
    """

    # Authentication credentials
    SECRET_KEY: str = settings.JWT_SECRET_KEY
    REFRESH_KEY: str = settings.JWT_REFRESH_KEY

    # JWT configuration
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES or 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES or 10080  # [7 days]

    # Security headers and CORS settings
    CORS_ORIGINS: List[str] = settings.CORS_ORIGINS.split(",") or [settings.FRONTEND_BASE_URL]

    SECURITY_HEADERS: Dict[str, str] = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
    }

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 900  # 15 minutes in seconds

    @classmethod
    def get_secret_key(cls) -> str:
        """
        Returns the secret key used for cryptographic operations.

        Returns:
            str: The configured secret key for cryptographic operations
        """
        return cls.SECRET_KEY

    @classmethod
    def get_jwt_config(cls) -> Dict[str, Any]:
        """
        Returns JWT configuration parameters as a dictionary.

        Returns:
            Dict[str, Any]: Dictionary containing JWT algorithm and expiration settings
                - algorithm (str): JWT algorithm
                - access_token_expire_minutes (int): Access token expiration in minutes
                - refresh_token_expire_days (int): Refresh token expiration in days
        """
        return {
            "algorithm": cls.ALGORITHM,
            "access_token_expire_minutes": cls.ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_expire_minutes": cls.REFRESH_TOKEN_EXPIRE_MINUTES,
        }

    @classmethod
    def get_security_headers(cls) -> Dict[str, str]:
        """
        Returns security headers configuration.

        Returns:
            Dict[str, str]: Dictionary containing security headers with their values
        """
        return cls.SECURITY_HEADERS.copy()

    @classmethod
    def get_cors_config(cls) -> Dict[str, Any]:
        """
        Returns CORS configuration for the application.

        Returns:
            Dict[str, Any]: Dictionary containing CORS settings with the following keys:
                - allow_origins (list): List of allowed origins
                - allow_credentials (bool): Whether to allow credentials
                - allow_methods (list): List of allowed HTTP methods
                - allow_headers (list): List of allowed HTTP headers
        """
        return {
            "allow_origins": cls.CORS_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }


@lru_cache
def load_security_config() -> SecurityConfig:
    """
    Loads and caches the security configuration using LRU cache.

    Returns:
        SecurityConfig: Cached instance of SecurityConfig class
    """
    security_config = SecurityConfig()
    return security_config


# Global security settings instance:
security_settings: SecurityConfig = load_security_config()
