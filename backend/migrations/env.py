from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from src.portfolio.models.models import Base

import os
import sys
from src.core.settings import settings

sys.path.append(os.path.join(sys.path[0], 'src'))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section

config.set_section_option(section, "postgres_user", settings.db.postgres_user)
config.set_section_option(section, "postgres_host", settings.db.postgres_host)
config.set_section_option(section, "postgres_db", settings.db.postgres_db)
config.set_section_option(section, "postgres_port", str(settings.db.postgres_port))
config.set_section_option(section, "postgres_password", settings.db.postgres_password.get_secret_value())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()