from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import DATABASE_URL
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # ✅ Ensure this line exists


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # Test connections before reuse (fixes SSL errors)
    pool_recycle=3600,         # Recycle connections every hour (Neon timeout is 30min)
    connect_args={
        "connect_timeout": 10,  # Timeout for new connections
        "keepalives": 1,        # Enable TCP keepalives
        "keepalives_idle": 30,  # Start keepalives after 30s of idle
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
