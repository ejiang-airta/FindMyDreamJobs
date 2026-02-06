from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.config.settings import DATABASE_URL
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # ✅ Ensure this line exists


# ✅ CORRECT CONNECTION POOL CONFIGURATION
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={"connect_timeout": 10}  # Only driver-level timeout
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
