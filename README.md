# 🎯 FindMyDreamJobs.com

An AI-powered job search assistant that helps users analyze job descriptions, match them with resumes, optimize content for ATS systems, and track applications — all through an intuitive, wizard-based web interface.

![GitHub stars](https://img.shields.io/github/stars/ejiang-airta/FindMyDreamJobs?style=social)
![GitHub forks](https://img.shields.io/github/forks/ejiang-airta/FindMyDreamJobs?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/ejiang-airta/FindMyDreamJobs?style=social)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=ejiang-airta.FindMyDreamJobs)

🌐 **Live Demo:** [https://findmydreamjobs.com](https://findmydreamjobs.com)

---

## 🚀 Features

* ✅ Upload resumes (PDF/DOCX/TXT)
* ✅ Analyze job descriptions
* ✅ Search for jobs with title and location i.e. engineer in Vancouver
* ✅ Evaluate ATS score for a resume
* ✅ Get match score against a job
* ✅ AI-optimized resume for download in .docx (watermarked if not reviewed by user)
* ✅ Track job applications with status
* ✅ Full onboarding wizard for first-time users
* ✅ Google or Email/Password authentication
* ✅ **JDI (Job Daily Intelligence)** — Automated job discovery from Gmail:
  * Connect Gmail via OAuth to scan for job alert emails (LinkedIn, Indeed, TrueUp)
  * Automatically extract job descriptions and calculate match scores
  * Daily shortlist of relevant jobs in dedicated JDI tab
  * Smart resume selection and personalized match reasons

---

## 🧱 Tech Stack

| Layer       | Tool                                                          |
| ----------- | ------------------------------------------------------------- |
| Frontend    | Next.js 15 + React 19 + TypeScript + Tailwind CSS v4 + shadcn/ui |
| Backend     | FastAPI (Python 3.11) + SQLAlchemy + Alembic                  |
| Database    | PostgreSQL (Neon managed service)                             |
| Auth        | NextAuth.js 4 (Google OAuth + Credentials)                    |
| AI/NLP      | OpenAI GPT-4o + spaCy + scikit-learn (TF-IDF)                 |
| Job API     | JSearch via RapidAPI                                          |
| Email       | Gmail API (OAuth 2.0, readonly scope)                         |
| Encryption  | Fernet (cryptography library) for token storage               |
| Hosting     | Render.com (frontend + backend services)                      |
| CI/CD       | GitLab CI/CD with PostgreSQL service container                |
| Testing     | Pytest (backend: 280 tests) + Playwright v1.57 (frontend: 44 E2E tests) |

---

## 🧑‍💻 Local Development Setup

### 1. Clone the repo

```bash
git clone https://github.com/ejiang-airta/FindMyDreamJobs.git
cd FindMyDreamJobs
```

### 2. Set up Python backend

```bash
cd backend
python -m venv job_env
source job_env/bin/activate
pip install -r requirements.txt
```

### 3. Set up frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

### 4. Environment variables

Create `.env` files in both `frontend` and `backend` with the following:

```env
# Example .env
DATABASE_URL=...
RENDER_API_KEY=...
FRONTEND_SERVICE_ID=...
BACKEND_SERVICE_ID=...
```

---

## 📦 Deployment

The app is deployed on Render with automatic preview environments for every pull request.

* **Production:** [https://findmydreamjobs.com](https://findmydreamjobs.com)
* **API:** [https://findmydreamjobs-service.onrender.com](https://findmydreamjobs-service.onrender.com)

---

## 🧪 Tests

```bash
# Backend tests
cd backend
pytest

# Frontend UI tests
cd frontend
npx playwright test
```

Tests run automatically in CI pipeline against Render preview environments.

---

## 🛣️ Roadmap

- [x] **JDI (Job Daily Intelligence)** — Automated job discovery from Gmail ✅ **LIVE** (Feb 2026)
- [ ] Add `/profile` and `/payment` pages
- [ ] Enhance resume download formatting
- [ ] Expand JDI to support more job sources (Glassdoor, ZipRecruiter, etc.)
- [ ] Add user analytics dashboard
- [ ] Stripe integration for paid users
- [ ] Email digest of top JDI matches

---

## 🤝 Contributing

Want to contribute? Feel free to fork the repo and open a Pull Request!

---

## 📄 License

MIT License

---

## 📊 GitHub Stats

![GitHub last commit](https://img.shields.io/github/last-commit/ejiang-airta/FindMyDreamJobs)
![GitHub issues](https://img.shields.io/github/issues/ejiang-airta/FindMyDreamJobs)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ejiang-airta/FindMyDreamJobs)