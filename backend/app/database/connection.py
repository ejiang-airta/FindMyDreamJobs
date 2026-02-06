from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.config.settings import DATABASE_URL
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # ✅ Ensure this line exists


# ✅ ADD CONNECTION POOL CONFIGURATION
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,           # Explicit pool class
    pool_size=5,                   # Max concurrent connections
    max_overflow=10,               # Extra connections when pool is full
    pool_pre_ping=True,            # Test connections before use
    connect_args={
        "connect_timeout": 10,     # Fail fast instead of hanging
        "options": "-c statement_timeout=30000"  # 30s query timeout
    }
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Add a print/debug log to verify which DB URL:
print("🔗 DATABASE_URL =", DATABASE_URL)


# ✅ Add this missing function if not present:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
