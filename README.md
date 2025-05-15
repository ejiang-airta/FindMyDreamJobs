# 🎯 FindMyDreamJobs.com

An AI-powered job search assistant that helps users analyze job descriptions, match them with resumes, optimize content for ATS systems, and track applications — all through an intuitive, wizard-based web interface.

---

## 🚀 Features

* ✅ Upload resumes (PDF/WORDX/TXT)
* ✅ Paste job descriptions
* ✅ Get match score & ATS score
* ✅ AI-enhanced resume optimization
* ✅ Download resumes (.docx, watermarked if not reviewed and approved by user)
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
| CI/CD    | (Planned) GitLab or GitHub Actions |
| Testing  | Pytest (backend) + Playwright (UI) |

---

## 🧑‍💻 Local Development Setup

### 1. Clone the repo

```bash
git clone https://gitlab.com/YOUR_USERNAME/Job_App.git
cd Job_App
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

The app is deployed on Render:

* **Frontend:** [https://findmydreamjobs.onrender.com](https://findmydreamjobs.onrender.com)
* **Backend:** [https://findmydreamjobs-service.onrender.com](https://findmydreamjobs-service.onrender.com)

Cron jobs automatically suspend services during off-hours to save cost.

---

## 🧪 Tests

* **Backend:** `pytest`
* **Frontend UI:** `playwright/test`
  Tests are executed manually (CI/CD coming soon).

---

## 🛣️ Roadmap

* [ ] Add `/profile` and `/payment` pages
* [ ] Enable GitLab CI to auto-test and deploy
* [ ] Enhance resume download formatting
* [ ] Add job search integration
* [ ] Add user analytics dashboard
* [ ] Stripe integration for paid users

---

## 🤝 Contributing

Want to contribute? Feel free to fork the repo and open a Merge Request!

---

## 📄 License

MIT License
