import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

print(f"ENV: {os.getenv('ENV')}")

if os.getenv("ENV") == "dev":
    load_dotenv(dotenv_path="../.env")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Obtener la URL de la base de datos de las variables de entorno
database_url = os.getenv('POSTGRES_URL')

print(f"POSTGRES_URL: {database_url}")

if not database_url:
    raise Exception("No se ha encontrado la variable de entorno POSTGRES_URL")

if database_url:
    config.set_main_option('sqlalchemy.url', database_url)

# Importar la Base y los modelos
sys.path = ['', '..'] + sys.path[1:]
from app.models import Base
from app import models

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is also acceptable
    here. By skipping the Engine creation we don't even need a
    DBAPI to be available.
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


def run_migrations_online():
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