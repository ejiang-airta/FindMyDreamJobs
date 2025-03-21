from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


username = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "password")
#host = os.getenv("POSTGRES_HOST", "localhost")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql+psycopg2://{username}:{password}@localhost/job_db")

print("DATABASE_URL")
print(DATABASE_URL)
