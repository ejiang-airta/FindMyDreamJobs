# 🛠️ Local Development & Deployment Guide

This guide walks you through setting up and running the **FindMyDreamJobs.com** project on your local machine, including frontend, backend, database, and environment configuration.

---

## 🧱 Project Structure

```
Job_App/
├── backend/                  # FastAPI app
├── frontend/                 # Next.js app
├── resume_service.sh         # Cron job script to resume frontend/backend service on render
├── suspend_service.sh        # Cron job script to suspend frontend/backend service on render
├── .gitlab-ci.yml (planned) # CI/CD pipeline
└── docs/setup.md             # You're here!
```

---

## 🔧 Prerequisites

* Python 3.11+
* Node.js 18+
* PostgreSQL (local or hosted on Neon)
* Git
* VS Code (optional but recommended)

---

## 🧪 Backend Setup (FastAPI)

```bash
cd backend
python -m venv job_env
source job_env/bin/activate
pip install -r requirements.txt
```

Create `.env` file in `backend/`:

```env
DATABASE_URL=postgresql+psycopg2://user:password@host/dbname
RENDER_API_KEY=your_render_api_key
FRONTEND_SERVICE_ID=srv-frontend-id
BACKEND_SERVICE_ID=srv-backend-id
```

Start the backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 💻 Frontend Setup (Next.js)

```bash
cd frontend
npm install
```

Create `.env.local` in `frontend/`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_secret
```

Start the frontend:

```bash
npm run dev
```

---

## 🧪 Run Tests

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npx playwright test
```

---

## 🚀 Deploy to Render

1. Push your latest changes to GitLab/GitHub
2. Enable auto-deploy for frontend and backend services
3. Set the environment variables in Render for both services
4. Verify cron jobs (suspend/resume) reference the correct branch and script path

---

## 🧹 Cron Job Scripts (Render)

**resume_service.sh**

```bash
curl -X POST "https://api.render.com/v1/services/${FRONTEND_SERVICE_ID}/resume" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"
curl -X POST "https://api.render.com/v1/services/${BACKEND_SERVICE_ID}/resume" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"
```

**suspend_service.sh**

```bash
curl -X POST "https://api.render.com/v1/services/${FRONTEND_SERVICE_ID}/suspend" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"
curl -X POST "https://api.render.com/v1/services/${BACKEND_SERVICE_ID}/suspend" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"
```

---

## ✅ Next Steps

* Implement CI/CD via GitLab CI or GitHub Actions
* Expand user dashboard, profile, and payment features
* Add production monitoring and alerts