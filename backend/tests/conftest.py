"""
Shared test fixtures -- real PostgreSQL with per-test transaction rollback.

Environment-aware:
  - Local:     TEST_DATABASE_URL defaults to postgresql+psycopg2://job_user@localhost/job_db_test
  - GitLab CI: TEST_DATABASE_URL is set by the pipeline (postgres service container)
"""

import os
import pytest
from datetime import datetime, timezone

# Set dummy env vars BEFORE importing app (OpenAI client initializes at import time)
os.environ.setdefault("OPENAI_API_KEY", "sk-test-dummy-key-for-testing")
os.environ.setdefault("RAPIDAPI_KEY", "test-dummy-rapidapi-key")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.database.connection import Base, get_db
from app.main import app
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.application import Application
from app.models.match import JobMatch
from app.models.saved_job import SavedJob

# ---------------------------------------------------------------------------
# Database engine -- reads TEST_DATABASE_URL with local fallback
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://job_user@localhost/job_db_test",
)

engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# ---------------------------------------------------------------------------
# Session-scoped: create / drop all tables once per test session
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables at the start of the test session, drop at the end."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------------------------
# Per-test: transactional isolation (rollback after each test)
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_session():
    """Yield a DB session wrapped in a transaction that is rolled back."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ---------------------------------------------------------------------------
# FastAPI TestClient with overridden get_db
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(db_session):
    """TestClient that uses the test DB session (with rollback)."""

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass  # session lifecycle handled by db_session fixture

    # Override every get_db in the app
    app.dependency_overrides[get_db] = _override_get_db

    # Also override the local get_db functions defined in route modules
    from app.routes import resume as resume_mod
    from app.routes import match as match_mod
    from app.routes import application as app_mod
    from app.routes import ats as ats_mod
    from app.routes import ai_optimization as ai_mod
    from app.routes import user as user_mod

    for mod in [resume_mod, match_mod, app_mod, ats_mod, ai_mod, user_mod]:
        if hasattr(mod, "get_db"):
            app.dependency_overrides[mod.get_db] = _override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Data factories
# ---------------------------------------------------------------------------

@pytest.fixture()
def test_user(db_session):
    """Insert a test user and return it."""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = User(
        email="testuser@example.com",
        full_name="Test User",
        hashed_password=pwd_context.hash("testpassword123"),
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture()
def test_resume(db_session, test_user):
    """Insert a test resume and return it."""
    resume = Resume(
        user_id=test_user.id,
        resume_name="test_resume.txt",
        file_path="uploads/resumes/test_resume.txt",
        parsed_text=(
            "John Doe\njohn@email.com\n\nExperience\n"
            "Senior Software Engineer at Acme Corp\n"
            "- Built microservices with Python, FastAPI, PostgreSQL\n"
            "- Led team of 5 engineers\n\n"
            "Skills\nPython, JavaScript, AWS, Docker, Kubernetes, React"
        ),
        ats_score_initial=65.0,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(resume)
    db_session.flush()
    return resume


@pytest.fixture()
def test_job(db_session, test_user):
    """Insert a test job and return it."""
    job = Job(
        user_id=test_user.id,
        job_title="Senior Software Engineer",
        company_name="Tech Corp",
        location="Toronto, ON",
        job_description=(
            "We are looking for a Senior Software Engineer with experience in "
            "Python, FastAPI, PostgreSQL, Docker, and Kubernetes. AWS experience "
            "is a plus. You will build microservices and lead a small team."
        ),
        extracted_skills={
            "skills": [
                {"skill": "Python", "frequency": 3},
                {"skill": "FastAPI", "frequency": 2},
                {"skill": "PostgreSQL", "frequency": 2},
                {"skill": "Docker", "frequency": 1},
                {"skill": "Kubernetes", "frequency": 1},
                {"skill": "AWS", "frequency": 1},
            ],
            "emphasized_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
        salary="$140,000 - $180,000",
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(job)
    db_session.flush()
    return job


@pytest.fixture()
def test_match(db_session, test_user, test_resume, test_job):
    """Insert a test job match and return it."""
    match = JobMatch(
        user_id=test_user.id,
        job_id=test_job.id,
        resume_id=test_resume.id,
        match_score_initial=75.5,
        matched_skills="Python,FastAPI,PostgreSQL",
        missing_skills="Kubernetes",
        ats_score_initial=65.0,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(match)
    db_session.flush()
    return match
