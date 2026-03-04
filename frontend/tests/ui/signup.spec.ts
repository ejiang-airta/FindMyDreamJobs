// File: frontend/tests/ui/signup.spec.ts
import { test, expect } from '@playwright/test'
import { BASE_URL } from './test-config'

test.describe('Signup', () => {

  test('Test# 28: Signup page renders with all fields', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    await expect(page.getByRole('heading', { name: /Create New Account/ })).toBeVisible()
    await expect(page.locator('input[type="text"]')).toBeVisible()  // Full name
    await expect(page.locator('input[type="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
    await expect(page.locator('button', { hasText: 'Create Account' })).toBeVisible()
  })

  test('Test# 29: Signup page has link to login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    const signInLink = page.locator('a', { hasText: 'Sign In' })
    await expect(signInLink).toBeVisible()
    await signInLink.click()
    await expect(page).toHaveURL(/.*login/)
  })

  test('Test# 30: Missing fields in signup show alert', async ({ page }) => {
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('Please enter all fields.')
      await dialog.dismiss()
    })

    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    // Only fill email, leave name and password empty
    await page.fill('input[type="email"]', 'test@example.com')
    await page.locator('button', { hasText: 'Create Account' }).click()
  })

  test('Test# 31: Full signup workflow', async ({ page }) => {
    test.setTimeout(60000) // Extended: preview cold start + React hydration + real signup + signIn

    const timestamp = Date.now()
    const testEmail = `testuser_${timestamp}@example.com`
    const testPassword = 'TestPassword123!'
    const testName = `Test User ${timestamp}`

    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    // Wait for React to fully hydrate before filling.
    // In preview (slow network + large JS bundles), domcontentloaded fires before React has
    // attached onChange handlers. If we fill too early, React state stays empty and the form
    // submit fires alert("Please enter all fields.") instead of calling fetch().
    // __reactFiber$ properties appear on DOM nodes only after React.hydrateRoot() completes.
    await page.waitForFunction(() => {
      const el = document.querySelector('input[type="email"]')
      return el !== null && Object.keys(el).some(k => k.startsWith('__react'))
    }, { timeout: 30000 })

    // Fill in all fields
    await page.fill('input[type="text"]', testName)
    await page.fill('input[type="email"]', testEmail)
    await page.fill('input[type="password"]', testPassword)

    // Verify all fields are filled
    await expect(page.locator('input[type="text"]')).toHaveValue(testName)
    await expect(page.locator('input[type="email"]')).toHaveValue(testEmail)
    await expect(page.locator('input[type="password"]')).toHaveValue(testPassword)

    // Click Create Account — real signup creates user in DB, signIn auto-logs in, redirects to home
    await page.locator('button', { hasText: 'Create Account' }).click()
    await page.waitForURL(/\/(home|dashboard|$)/, { timeout: 30000 })
  })

})
