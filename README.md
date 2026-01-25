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

---

## 🧱 Tech Stack

| Layer    | Tool                               |
| -------- | ---------------------------------- |
| Frontend | Next.js + Tailwind CSS + shadcn    |
| Backend  | FastAPI (Python)                   |
| Database | PostgreSQL (hosted on Neon)        |
| Auth     | NextAuth.js                        |
| Hosting  | Render.com                         |
| CI/CD    | GitLab CI + Playwright             |
| Testing  | Pytest (backend) + Playwright (UI) |

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

- [ ] Add `/profile` and `/payment` pages
- [ ] Enhance resume download formatting
- [ ] Add job search integration (LinkedIn, Indeed)
- [ ] Add user analytics dashboard
- [ ] Stripe integration for paid users

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