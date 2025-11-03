import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings configuration using Pydantic BaseSettings.

    This class defines all application configuration parameters with appropriate
    defaults. Settings are loaded from environment variables and .env files.

    Attributes:
        ENVIRONMENT: Current environment (development, production, etc.)
        BASE_DIR: Base directory of the application
        PUBLIC_ROUTES: Set of public routes that don't require authentication

        BACKEND_BASE_URL: Base URL for backend application
        FRONTEND_BASE_URL: Base URL for frontend application
        CORS_ORIGINS: Comma seperated allowed cors url strings

        DB_USER: Database username
        DB_PASSWORD: Database password
        DB_HOST: Database host
        DB_PORT: Database port
        DB_NAME: Database name

        REDIS_REST_URL: Upstash redis REST URL
        REDIS_REST_TOKEN: Upstash redis REST Token

        AWS_ACCESS_KEY: AWS access key for cloud services
        AWS_SECRET_ACCESS_KEY: AWS secret access key
        AWS_REGION: AWS region for services
        AWS_BUCKET_NAME: S3 bucket name for file storage

        GOOGLE_API_KEY: API key for Google AI services
        LLM_EMBEDDING_MODEL: Language model to use for AI embedding operations
        LLM_CHAT_MODEL: Language model to use for AI chat operations
        FAISS_INDEX_PATH: Path to store/load FAISS index files
        EMBEDDING_DIMENSION: Dimension of embedding vectors
        BATCH_SIZE: Default batch size for embedding operations
        TOP_K_RESULTS: Default number of search results to return

        API_PREFIX: API endpoint prefix
        API_KEY: Application API key for authentication
        SECRET_KEY: Secret key for cryptographic operations
        TOKEN_EXPIRY: Token expiration time in minutes
        DEFAULT_PAGE: Default pagination page number
        DEFAULT_PAGE_LIMIT: Default pagination limit
        DEFAULT_OFFSET: Default pagination offset

        LOG_ROTATION: Log rotation schedule
        LOG_RETENTION: Log retention period
        DATABASE_URL: Async SQLAlchemy database connection URL
    """

    # Environment type
    APP_ENV: str = "development"

    # Root directory and URLs
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    PUBLIC_ROUTES: set[str] = {
        "/",
        "/health",
        "/metrics",
        "/favicon.ico",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/user/register",
        "/api/v1/user/login",
    }
    BACKEND_BASE_URL: str = "http://localhost:8000"
    FRONTEND_BASE_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:3000"

    # Database Configuration with defaults from environment variables
    DB_USER: str = "postgres"
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"

    # Redis Credentials
    REDIS_REST_URL: str
    REDIS_REST_TOKEN: str

    # AWS Credentials
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "ap-south-1"
    AWS_BUCKET_NAME: str

    # AI/ML Configuration
    GOOGLE_API_KEY: str
    LLM_EMBEDDING_MODEL: str = "gemini-embedding-001"
    LLM_CHAT_MODEL: str = "gemini-2.5-pro"
    EMBEDDING_DIMENSION: int = 3072
    BATCH_SIZE: int = 1000
    TOP_K_RESULTS: int = 5

    # Security Variables
    JWT_SECRET_KEY: str
    JWT_REFRESH_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    # Global Variables
    API_PREFIX: str = "/api/v1"
    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_LIMIT: int = 10
    DEFAULT_OFFSET: int = 0

    # Log settings
    LOG_ROTATION: str = "00:00"
    LOG_RETENTION: str = "30 days"

    # Computed properties
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def CHROMA_STORAGE_PATH(self) -> str:
        return f"{self.BASE_DIR}/data/chromadb"

    # Configure the location of the .env file (based on environment)
    model_config = SettingsConfigDict(
        env_file=".env.development", case_sensitive=False, extra="ignore"
    )


@lru_cache
def load_settings(environment: str = "development") -> Settings:
    env_file = f".env.{environment}"
    settings = Settings(_env_file=env_file)
    return settings


# Global settings instance:
environment: str = os.getenv("APP_ENV", "development")
settings: Settings = load_settings(environment)
