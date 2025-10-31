from app.core import settings
from .database import DatabaseConfig, DatabaseManager


class DatabaseSessionManager:
    """
    Singleton pattern for database session manager.
    This ensures a single instance of `DatabaseConfig` and `DatabaseManager` is used.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            db_config = DatabaseConfig(settings.DATABASE_URL)
            cls._instance.db_manager = DatabaseManager(db_config)
        return cls._instance

    @property
    def get_db(self):
        """Expose the `get_db` method of the DatabaseManager."""
        return self.db_manager.get_db

    @property
    def lifespan(self):
        """Expose the `lifespan` method of the DatabaseManager."""
        return self.db_manager.lifespan

    @property
    def get_db_asynchronous(self):
        """Expose the `get_db_asynchronous` context manager for middleware."""
        return self.db_manager.get_db_asynchronous

    @property
    def get_db_synchronous(self):
        """Expose the `get_db_synchronous` method of the DatabaseManager."""
        return self.db_manager.get_db_synchronous


# Global instance for easy access
db_session_manager = DatabaseSessionManager()