from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.config.settings import DATABASE_URL
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # ✅ Ensure this line exists


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # Test connections before reuse (detects stale SSL connections)
    pool_recycle=1500,         # Recycle at 25 min — before Neon's ~30 min idle timeout
    connect_args={
        "connect_timeout": 10,  # Timeout for new connections
        "keepalives": 1,        # Enable TCP keepalives
        "keepalives_idle": 30,  # Start keepalive probes after 30s of idle
        "keepalives_interval": 10,  # Send a probe every 10s (OS default is 75s — too slow)
        "keepalives_count": 5,      # 5 failed probes → close connection (OS default is 9)
    }
)

@event.listens_for(engine, "handle_error")
def handle_ssl_disconnect(context):
    """Safety net: explicitly invalidate connections closed by Neon's SSL idle timeout.

    pool_pre_ping catches most stale connections, but a race condition is possible
    (pre-ping succeeds, Neon closes SSL in the gap before the actual query).
    Setting is_disconnect=True ensures the bad connection is removed from the pool
    so future requests get a fresh one.
    """
    if "SSL connection has been closed unexpectedly" in str(context.original_exception):
        context.is_disconnect = True

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
