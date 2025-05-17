import { Page } from '@playwright/test'

export async function loginAsTestUser(page: Page, env: string) {
  const BASE_URL = env === 'dev'
    ? 'http://localhost:3000'
    : 'https://findmydreamjobs.com'
  console.log("Base URL: ", BASE_URL)

  const email = process.env.E2E_EMAIL || 'testuser@abc.com'
  const password = process.env.E2E_PASSWORD || 'test123'

  async function tryLogin() {
    await page.goto(`${BASE_URL}/login`)
    await page.fill('input[type="email"]', email)
    await page.fill('input[type="password"]', password)
    await page.locator('button', { hasText: 'Sign In' }).click()
    await page.getByText('Welcome back, test user1!').waitFor({ timeout: 20000 })
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
