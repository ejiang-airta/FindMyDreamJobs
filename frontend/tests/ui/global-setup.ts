// ✅ File: frontend/tests/ui/global-setup.ts
import { chromium, request } from '@playwright/test'
import { BASE_URL, BACKEND_URL, TIMEOUT_MS, INTERVAL_MS } from './test-config'

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

export default async function globalSetup() {
  console.log(`\n🌙 Render Preview Warmup Start`)
  console.log(`📍 Target Frontend: ${BASE_URL}`)
  console.log(`📍 Target Backend: ${BACKEND_URL}\n`)

  await waitForBackend()
  await waitForFrontend()
  
  console.log('🔥 Warmup complete. All Preview services are LIVE. Starting tests.\n')
}