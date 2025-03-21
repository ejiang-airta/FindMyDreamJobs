from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import DATABASE_URL
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # ✅ Ensure this line exists


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)