// ✅ File: frontend/tests/ui/global-setup.ts
import { chromium, request } from '@playwright/test'
import { BASE_URL, BACKEND_URL, TEST_ENV, TIMEOUT_MS, INTERVAL_MS } from './test-config'

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

async function waitForBackend() {
  console.log(`⏳ Waiting for Backend Preview: ${BACKEND_URL}...`)
  const start = Date.now()
  const api = await request.newContext()

  while (Date.now() - start < TIMEOUT_MS) {
    try {
      const res = await api.get(`${BACKEND_URL}/`)
      if (res.ok()) {
        const json = await res.json().catch(() => null)
        // Adjust this check based on your actual health check response
        if (json?.message?.includes('Welcome to FindMyDreamJobs API') || res.status() === 200) {
          console.log(`✅ Backend ready: ${BACKEND_URL}`)
          await api.dispose()
          return
        }
      }
      console.log(`… Backend not ready yet (${res.status()})`)
    } catch {
      console.log(`… Backend not ready yet (connecting...)`)
    }
    await sleep(INTERVAL_MS)
  }

  await api.dispose()
  throw new Error(`❌ Backend did not become ready within ${TIMEOUT_MS}ms`)
}


async function waitForFrontend() {
  console.log(`⏳ Waiting for Frontend Preview: ${BASE_URL}...`)
  const start = Date.now()
  const browser = await chromium.launch()
  const page = await browser.newPage()

  while (Date.now() - start < TIMEOUT_MS) {
    try {
      // We use a shorter timeout here so the loop can retry faster
      await page.goto(BASE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 })

      // pick either of these:
      const hasHeroText = await page.getByText('Find Your Dream Job').first().isVisible().catch(() => false)
      // or: const hasHomeMenu = await page.getByRole('link', { name: 'Home' }).isVisible().catch(() => false)

      if (hasHeroText) {
        console.log(`✅ Frontend ready: ${BASE_URL}`)
        await browser.close()
        return
      }
      console.log(`… Frontend loaded but Hero text not visible yet`)
    } catch {
      console.log(`… Frontend not responding yet (Render is likely still building)`)
    }

    await sleep(INTERVAL_MS)
  }

  await browser.close()
  throw new Error(`❌ Frontend did not become ready within ${TIMEOUT_MS}ms`)
}

// Seed the E2E test user into the preview DB after alembic runs on a fresh Neon branch.
// In production the user already exists; in dev it's created manually.
// Only runs in preview so it never fires against the production DB.
async function seedTestUser() {
  const email    = process.env.E2E_EMAIL    || 'testuser@abc.com'
  const password = process.env.E2E_PASSWORD || 'test123'
  const backendBase = BACKEND_URL.replace(/\/$/, '')

  console.log(`🌱 Seeding test user (${email}) into preview DB...`)
  const api = await request.newContext()
  try {
    const res = await api.post(`${backendBase}/auth/signup`, {
      data: { email, password, full_name: 'test user1' }
    })
    if (res.ok()) {
      console.log(`✅ Test user created`)
    } else {
      const body = await res.json().catch(() => ({}))
      const detail = String(body.detail || '').toLowerCase()
      if (res.status() === 400 && detail.includes('already')) {
        console.log(`ℹ️  Test user already exists (idempotent)`)
      } else {
        console.warn(`⚠️  Unexpected response seeding test user: HTTP ${res.status()} — ${body.detail}`)
      }
    }
  } catch (e) {
    console.warn(`⚠️  Could not seed test user (non-fatal): ${e}`)
  } finally {
    await api.dispose()
  }
}

export default async function globalSetup() {
  console.log(`\n🌙 Render Preview Warmup Start`)
  console.log(`📍 Target Frontend: ${BASE_URL}`)
  console.log(`📍 Target Backend: ${BACKEND_URL}\n`)

  await waitForBackend()

  // Seed test user only in preview — fresh Neon DB has no users yet.
  // Runs after backend is healthy so the signup endpoint is ready.
  if (TEST_ENV === 'preview') {
    await seedTestUser()
  }

  await waitForFrontend()

  console.log('🔥 Warmup complete. All Preview services are LIVE. Starting tests.\n')
}