import { chromium, request } from '@playwright/test'

const TEST_ENV = process.env.ENV || 'prod'

const FRONTEND_URL =
  TEST_ENV === 'dev' ? 'http://localhost:3000' : 'https://findmydreamjobs.com'

const BACKEND_URL =
  TEST_ENV === 'dev' ? 'http://localhost:8000' : 'https://findmydreamjobs.onrender.com'

const TIMEOUT_MS = Number(process.env.WARMUP_TIMEOUT_MS || 180000) // 3 min
const INTERVAL_MS = Number(process.env.WARMUP_INTERVAL_MS || 5000) // 5 sec

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

async function waitForBackend() {
  const start = Date.now()
  const api = await request.newContext()

  while (Date.now() - start < TIMEOUT_MS) {
    try {
      const res = await api.get(`${BACKEND_URL}/`)
      if (res.ok()) {
        const json = await res.json().catch(() => null)
        if (json?.message?.includes('Welcome to FindMyDreamJobs API')) {
          console.log(`✅ Backend ready: ${BACKEND_URL}`)
          await api.dispose()
          return
        }
      }
      console.log(`… Backend not ready yet (${res.status()})`)
    } catch {
      console.log(`… Backend not ready yet (network)`)
    }
    await sleep(INTERVAL_MS)
  }

  await api.dispose()
  throw new Error(`❌ Backend did not become ready within ${TIMEOUT_MS}ms`)
}

async function waitForFrontend() {
  const start = Date.now()
  const browser = await chromium.launch()
  const page = await browser.newPage()

  while (Date.now() - start < TIMEOUT_MS) {
    try {
      await page.goto(FRONTEND_URL, { waitUntil: 'domcontentloaded', timeout: 60000 })

      // pick either of these:
      const hasHeroText = await page.getByText('Find Your Dream Job').first().isVisible().catch(() => false)
      // or: const hasHomeMenu = await page.getByRole('link', { name: 'Home' }).isVisible().catch(() => false)

      if (hasHeroText) {
        console.log(`✅ Frontend ready: ${FRONTEND_URL}`)
        await browser.close()
        return
      }

      console.log(`… Frontend loaded but not ready yet`)
    } catch {
      console.log(`… Frontend not ready yet (loading)`)
    }

    await sleep(INTERVAL_MS)
  }

  await browser.close()
  throw new Error(`❌ Frontend did not become ready within ${TIMEOUT_MS}ms`)
}

export default async function globalSetup() {
  console.log(`\n🌙 Render warmup start (ENV=${TEST_ENV})`)
  await waitForBackend()
  await waitForFrontend()
  console.log('🔥 Warmup complete. Starting tests.\n')
}
