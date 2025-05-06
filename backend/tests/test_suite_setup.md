# ✅ Test Suite Setup

## Phase A – Test Infrastructure & Automation Coverage

### ✅ A1: Create Automated Tests

#### Unit Tests
- **Tools:** `pytest`
- **Targets:**
  - `resume_formatter.py`
  - `resume_optimizer.py`
  - `match.py`
- **Location:** `backend/tests/unit/`

#### API Tests
- **Tools:** `httpx` + `pytest`
- **Targets:**
  - `/upload-resume`
  - `/analyze-job`
  - `/match-score`
  - `/optimize-resume`
  - `/approve-resume`
- **Location:** `backend/tests/api/`

#### UI Tests (Lightweight, Alpha)
- **Tools:** `Playwright`
- **Targets:**
  - Upload Resume flow
  - Match Score calculation
  - Optimization + Apply wizard
- **Location:** `frontend/tests/ui/`

---

### 🛠️ A2: CI/CD Integration
- Configure GitLab CI
- Add `run: pytest` step for both unit + API tests
- Add `npx playwright test` for UI smoke checks
- Auto-deploy only if all tests pass

---

### 📖 A3: Dev Documentation
- Generate `README.md` with project overview and local setup
- Add `docs/setup.md` with production deployment, environment config, and troubleshooting
- Optional: Add a `/help` route in frontend with short video guides + usage tips

---

## Phase B – Post-MVP Enhancements

### 👤 B1: User Profile Page
- Store/display user name/email
- Add change password functionality

### 💳 B2: Payment Integration
- Basic Stripe setup for Premium subscription
- Tiered feature restrictions based on plan

### 📣 B3: Growth & Marketing Plan
- Landing Page revamp
- Beta user funnel
- Optional integration with analytics tools (GA or Plausible)

---

Let’s go build something amazing! 🚀
