#  File: /backend/app/config/skills_config.py
#  ✅ Central list of technical skills for NLP extraction
SKILL_KEYWORDS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "Kotlin",
    "HTML", "CSS", "SQL", "NoSQL", "PostgreSQL", "MongoDB", "MySQL", "Redis", 
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", 
    "React", "Next.js", "Vue", "Angular", "Node.js", "Express", "Flask", "Django", "Spring Boot",
    "REST", "GraphQL", "gRPC", "FastAPI",
    "Kafka", "RabbitMQ", "Celery",
    "Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn",
    "Linux", "Shell", "Git", "Jira",
    "Agile", "Scrum", "DevOps", "SRE", "Security", "Monitoring", "Testing",
    "AI/ML", "AI", "Artificial Intelligence", "Machine Learning", "NLP", "LLM",
    "Data Science",
    "Selenium", "Automation Framework",
]
# ✅ Centralized config for skill frequency logic to be used in /rountes/job.py:
MIN_SKILL_FREQUENCY = 2     # minmum number of frequency to count for emphasized skills
MAX_EMPHASIZED_SKILLS = 5   # maximum number of record to be stored as emphasized skills