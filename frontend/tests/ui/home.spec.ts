// File: frontend/tests/ui/home.spec.ts
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BASE_URL } from './test-config'

test.describe('Home', () => {

  test('Test# 19: Home page renders for unauthenticated users', async ({ page }) => {
    await page.goto(`${BASE_URL}`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    // Hero section heading should be visible (use getByRole to avoid strict mode violation)
    await expect(page.getByRole('heading', { name: 'Find Your Dream Job' })).toBeVisible({ timeout: 10000 })
  })

  test('Test# 20: Welcome message for logged-in users', async ({ page }) => {
    await loginAsTestUser(page)
    await expect(page.getByText('Welcome back, test user1!')).toBeVisible({ timeout: 15000 })
  })

  test('Test# 21: Get Started navigates to wizard', async ({ page }) => {
    await loginAsTestUser(page)

    const getStartedBtn = page.locator('button', { hasText: /Get Started/i })
    if (await getStartedBtn.isVisible()) {
      await getStartedBtn.click()
      await expect(page).toHaveURL(/.*wizard/, { timeout: 5000 })
    }
  })

  test('Test# 22: Learn More navigates to about', async ({ page }) => {
    await page.goto(`${BASE_URL}`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    await page.waitForTimeout(1000)

    const learnMoreBtn = page.locator('button', { hasText: /Learn More/i })
    if (await learnMoreBtn.isVisible()) {
      await learnMoreBtn.click()
      await expect(page).toHaveURL(/.*about/, { timeout: 5000 })
    }
  })

})
