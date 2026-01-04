// ✅ File: frontend/tests/ui/global-setup.ts
import { chromium, request } from '@playwright/test'

const TEST_ENV = process.env.ENV || 'prod'

// 1. UPDATED URL LOGIC: Matches your render.yaml naming
const FRONTEND_URL =
  process.env.PLAYWRIGHT_BASE_URL || 
  (TEST_ENV === 'dev' ? 'http://localhost:3000' : 'https://findmydreamjobs.com')

const BACKEND_URL =
  process.env.PLAYWRIGHT_BACKEND_URL || 
  (TEST_ENV === 'dev' ? 'http://localhost:8000' : 'https://findmydreamjobs.onrender.com/')

const TIMEOUT_MS = Number(process.env.WARMUP_TIMEOUT_MS || 420000) // Increased to 7 min for Render builds
const INTERVAL_MS = Number(process.env.WARMUP_INTERVAL_MS || 10000) // 10 sec intervals to be gentler

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
  console.log(`⏳ Waiting for Frontend Preview: ${FRONTEND_URL}...`)
  const start = Date.now()
  const browser = await chromium.launch()
  const page = await browser.newPage()

  while (Date.now() - start < TIMEOUT_MS) {
    try {
      // We use a shorter timeout here so the loop can retry faster
      await page.goto(FRONTEND_URL, { waitUntil: 'domcontentloaded', timeout: 30000 })

      // pick either of these:
      const hasHeroText = await page.getByText('Find Your Dream Job').first().isVisible().catch(() => false)
      // or: const hasHomeMenu = await page.getByRole('link', { name: 'Home' }).isVisible().catch(() => false)

      if (hasHeroText) {
        console.log(`✅ Frontend ready: ${FRONTEND_URL}`)
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

export default async function globalSetup() {
  // 2. REMOVED THE SKIP LOGIC: 
  // We wait for the preview to finish building.
  
  console.log(`\n🌙 Render Preview Warmup Start`)
  console.log(`📍 Target Frontend: ${FRONTEND_URL}`)
  console.log(`📍 Target Backend: ${BACKEND_URL}\n`)

  await waitForBackend()
  await waitForFrontend()
  
  console.log('🔥 Warmup complete. All Preview services are LIVE. Starting tests.\n')
}
