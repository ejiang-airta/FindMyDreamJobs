from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.application import Application
from app.models.match import JobMatch

import datetime

def seed_data():
    db: Session = SessionLocal()

    try:
        # Seed Users
        user = User(
            email="jane.doe@example.com",
            hashed_password="fakehashedpw123",
            full_name="Jane Doe",
            created_at=str(datetime.datetime.now())
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Seed Resume
        resume = Resume(
            user_id=user.id,
            file_path="resumes/jane_doe.pdf",
            parsed_text="Python, FastAPI, PostgreSQL",
            created_at=datetime.datetime.now()
        )
        db.add(resume)

        # Seed Job
        job = Job(
            job_title="Senior Backend Engineer",
            company_name="Tech Corp",
            location="Remote",
            job_description="Looking for someone with experience in Python, FastAPI, and PostgreSQL.",
            job_url="https://techcorp.example.com/jobs/123",
            posted_date=datetime.datetime.now()
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Seed Application
        application = Application(
            user_id=user.id,
            job_id=job.id,
            resume_id=resume.id,
            application_url="https://techcorp.example.com/apply/123",
            application_status="In Progress",
            applied_date=datetime.datetime.now()
        )
        db.add(application)

        # Seed Match
        match = JobMatch(
            user_id=user.id,
            job_id=job.id,
            resume_id=resume.id,
            match_score=85.5,
            created_at=datetime.datetime.now()
        )
        db.add(match)

        db.commit()
        print("✅ Seeded database with test data.")

    except Exception as e:
        print("❌ Error seeding data:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()