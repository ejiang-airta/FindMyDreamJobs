// ✅ File: frontend/tests/ui/helpers.ts
import { Page } from '@playwright/test'
import { BASE_URL } from './test-config'

export async function loginAsTestUser(page: Page) {
  const email = process.env.E2E_EMAIL || 'testuser@abc.com'
  const password = process.env.E2E_PASSWORD || 'test123'

  async function tryLogin() {
    await page.goto(`${BASE_URL}/login`)
    await page.fill('input[type="email"]', email)
    await page.fill('input[type="password"]', password)
    await page.locator('button', { hasText: 'Sign In' }).click()
    await page.waitForLoadState('networkidle') // ensures all requests settle, use this to replace the message verification
    await page.waitForTimeout(1000) // wait for 1 seconds to ensure the message is displayed
    await page.getByText('Welcome back, test user1!').waitFor({ timeout: 15000 }) //ensure the message shows correctly after 'networkidle' state
  }

  try {
    await tryLogin()
  } catch (err) {
    console.warn('⚠️ First login attempt failed. Retrying...')
    try {
      await tryLogin()
    } catch (finalErr) {
      console.error('❌ Login failed after retry:', finalErr)
      // Optional: capture screenshot or page content
      const timestamp = Date.now()
      await page.screenshot({ path: `login-failure-${timestamp}.png`, fullPage: true })
      throw finalErr
    }
  }
}