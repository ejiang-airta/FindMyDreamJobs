from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine, pool
import sys
import os

# Ensure Python can find the app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import app settings and DB connection
from app.config.settings import DATABASE_URL
from app.database.connection import Base  # ✅ Ensure Base is imported
# Import all models so Alembic can see them
from app.models import user, resume, job, application, match # ✅ Import all models or else Alembic can't see them

# Alembic Config
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# ✅ Provide Alembic with SQLAlchemy models
target_metadata = Base.metadata  # ✅ THIS FIXES THE ERROR

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
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
