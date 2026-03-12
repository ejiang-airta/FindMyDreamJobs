// File: frontend/tests/ui/login.spec.ts
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BASE_URL, TEST_ENV } from './test-config'

test.describe('Login', () => {

  test('Test# 1: User can visit login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    await expect(page.locator('input[type="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
    await expect(page.locator('button', { hasText: 'Sign In' })).toBeVisible()
  })

  test('Test# 2: Login fails with incorrect credentials', async ({ page }) => {
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('Please enter both email and password.')
      await dialog.dismiss()
    })

    await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    await page.fill('input[type="email"]', 'fakeuser@example.com')
    await page.fill('input[type="password"]', 'wrongpassword')
    await page.locator('button', { hasText: 'Sign In' }).click()
  })

  test('Test# 3: Login succeeds with right credentials', async ({ page }) => {
    await loginAsTestUser(page)
    await expect(page.getByText('Welcome back, test user1!')).toBeVisible({ timeout: 15000 })
  })

  test('Test# 4: Navigate to Dashboard page', async ({ page }) => {
    await loginAsTestUser(page)

    // Wait for post-login navigation to fully settle on home page before clicking nav
    await page.waitForURL(`${BASE_URL}/`, { timeout: 5000 }).catch(() => {})
    await page.waitForLoadState('networkidle')

    const dashboardNavLink = page.locator('nav.bg-white :text("Dashboard")')
    await expect(dashboardNavLink).toBeVisible()
    await dashboardNavLink.click()

    // Use waitForURL (not toHaveURL) so navigation has time to complete
    await page.waitForURL(`${BASE_URL}/dashboard`, { timeout: 15000 })
    // Dashboard now shows a pipeline funnel card instead of the old "Tracked Applications" heading
    await expect(page.getByText('Application Pipeline')).toBeVisible({ timeout: 8000 })
  })

  test('Test# 5: Navigate to Analyze page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Analyze' }).click()
    await expect(page.getByRole('heading', { name: /Analyze Job Description/ })).toBeVisible({ timeout: 8000 })
  })

  test('Test# 6: Navigate to Match page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Match' }).click()
    await expect(page.getByRole('heading', { name: /Match Score/ }).first()).toBeVisible({ timeout: 8000 })
  })

  test('Test# 7: Navigate to Optimize page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Optimize' }).click()
    await expect(page.getByRole('heading', { name: /Optimize Resume/ })).toBeVisible({ timeout: 8000 })
  })

  test('Test# 8: Navigate to Apply page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Apply' }).click()
    await expect(page.getByRole('heading', { name: /Submit Job Application/ })).toBeVisible({ timeout: 8000 })
  })

  test('Test# 9: Navigate to Applications page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Applications' }).click()
    await expect(page.getByRole('heading', { name: /Your Job Applications/ })).toBeVisible({ timeout: 8000 })
  })

  test('Test# 10: Navigate to Stats page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Stats' }).click()
    await expect(page.getByRole('heading', { name: /Application Stats/ })).toBeVisible({ timeout: 8000 })
  })

  test('Test# 11: Navigate to Wizard page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Wizard' }).click()
    await expect(page.getByRole('heading', { name: /Smart Job Application Wizard/ })).toBeVisible({ timeout: 8000 })
  })

  test('Test# 12: Navigate back to Home page', async ({ page }) => {
    await loginAsTestUser(page)
    await page.getByRole('link', { name: 'Analyze' }).click()
    await page.getByRole('link', { name: 'Home' }).click()
    await expect(page.getByText('Welcome back, test user1!')).toBeVisible({ timeout: 15000 })
  })

})
