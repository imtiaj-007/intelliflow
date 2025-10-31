import asyncio
from logging.config import fileConfig

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.core import settings
from app.db.database import Base
from app.db.models import *

# Get the configuration from alembic.ini
config = context.config

# Ensure the logging configuration is set up
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Create a metadata object with naming convention
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

# Set the target metadata for Alembic to work with
target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Supabase schemas to exclude
EXCLUDE_SCHEMAS = {
    "auth",
    "extensions",
    "graphql",
    "graphql_public",
    "information_schema",
    "pgbouncer",
    "pg_catalog",
    "realtime",
    "storage",
    "vault",
}


def include_name(name, type_, parent_names):
    """Tell Alembic which schemas & objects to include."""
    # Skip excluded schemas
    if type_ == "schema":
        return name not in EXCLUDE_SCHEMAS

    # Skip objects belonging to excluded schemas
    if parent_names:
        schema = parent_names.get("schema")
        if schema in EXCLUDE_SCHEMAS:
            return False

    return True


def do_run_migrations(connection):
    """Run migrations using a synchronous connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,       # ensures schema-awareness
        include_name=include_name,  # exclude Supabase schemas safely
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' async mode."""
    configuration = config.get_section(config.config_ini_section)
    url = configuration["sqlalchemy.url"]

    connectable = create_async_engine(url, echo=False, future=True, pool_pre_ping=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Main entry point to start the migrations
if context.is_offline_mode():
    print("Offline mode is not supported for async migrations.")
else:
    # Run the migrations in an async event loop
    asyncio.run(run_migrations_online())