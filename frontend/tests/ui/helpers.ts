// File: frontend/tests/ui/helpers.ts
import { Page } from '@playwright/test'

export async function loginAsTestUser(page: Page, env: string) {
  const BASE_URL = env === 'dev'
    ? 'http://localhost:3000'
    : 'https://findmydreamjobs.com'
  console.log("Base URL: ", BASE_URL)
  await page.goto(`${BASE_URL}/login`)

  // login with a test user: 
  await page.fill('input[type="email"]', 'testuser@abc.com')
  await page.fill('input[type="password"]', 'test123')
  await page.locator('button', { hasText: 'Sign In' }).click()

  await page.getByText('Welcome back, test user1!').waitFor({ timeout: 5000 })
}
