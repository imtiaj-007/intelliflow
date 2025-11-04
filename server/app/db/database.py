from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.utils.logger import log


# Base Model for alembic
class Base(DeclarativeBase):
    """Base class for all models"""

    pass


class DatabaseConfig:
    def __init__(self, db_url: str):
        """Initialize database engine and sessionmaker."""
        # Synchronous engine and sessionmaker
        self.sync_engine = create_engine(
            db_url.replace("+asyncpg", "+psycopg2"), echo=False, future=True, poolclass=NullPool
        )
        self.SyncSessionLocal = sessionmaker(bind=self.sync_engine, expire_on_commit=False)

        # Asynchronous engine and sessionmaker
        self.async_engine = create_async_engine(
            db_url, echo=False, future=True, pool_pre_ping=True, poolclass=NullPool
        )
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.async_engine, expire_on_commit=False, class_=AsyncSession
        )


class DatabaseManager:
    def __init__(self, db_config: DatabaseConfig):
        self.config = db_config

    @contextmanager
    def get_db_synchronous(self) -> Generator[Session, None, None]:
        """
        Create a synchronous database session context manager.

        Returns:
            SQLAlchemy Session object for synchronous database operations
        """
        session = self.config.SyncSessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """
        Async lifespan context manager for the database.
        This initializes the database and ensures the connection is closed properly.
        """
        try:
            log.info("✅ Database connection established successfully.")
            yield
        except Exception as e:
            log.error(f"❌ Database startup error: {e}")
            raise
        finally:
            await self.config.async_engine.dispose()
            log.info("✅ Database connection closed.")

    @asynccontextmanager
    async def get_db_asynchronous(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Async context manager for middleware and other non-dependency contexts.
        Use this with 'async with' in middleware.
        """
        async with self.config.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {e}",
                )
            finally:
                await session.close()

    # For FastAPI dependency injection (async generator)
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Async generator for FastAPI dependency injection.
        Use this with Depends() in route handlers.
        """
        async with self.config.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except HTTPException:
                raise
            except Exception as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {e}",
                )
            finally:
                await session.close()