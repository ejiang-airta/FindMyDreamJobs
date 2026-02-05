// File: frontend/tests/ui/signup.spec.ts
import { test, expect } from '@playwright/test'
import { BASE_URL, BACKEND_URL } from './test-config'

test.describe('Signup Page', () => {

  test('signup-Test-28-Page-renders-form-fields', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    await expect(page.getByRole('heading', { name: /Create New Account/ })).toBeVisible()
    await expect(page.locator('input[type="text"]')).toBeVisible()  // Full name
    await expect(page.locator('input[type="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
    await expect(page.locator('button', { hasText: 'Create Account' })).toBeVisible()
  })

  test('signup-Test-29-Link-to-login-page', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    const signInLink = page.locator('a', { hasText: 'Sign In' })
    await expect(signInLink).toBeVisible()
    await signInLink.click()
    await expect(page).toHaveURL(/.*login/)
  })

  test('signup-Test-30-Missing-fields-alert', async ({ page }) => {
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('Please enter all fields.')
      await dialog.dismiss()
    })

    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    // Only fill email, leave name and password empty
    await page.fill('input[type="email"]', 'test@example.com')
    await page.locator('button', { hasText: 'Create Account' }).click()
  })

  test('signup-Test-31-Full-signup-workflow', async ({ page }) => {
    // Generate unique email to avoid conflicts with existing users
    const timestamp = Date.now()
    const testEmail = `testuser_${timestamp}@example.com`
    const testPassword = 'TestPassword123!'
    const testName = `Test User ${timestamp}`

    // Navigate to signup page first
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    // Fill in all fields
    await page.fill('input[type="text"]', testName)
    await page.fill('input[type="email"]', testEmail)
    await page.fill('input[type="password"]', testPassword)

    // Verify all fields are filled
    await expect(page.locator('input[type="text"]')).toHaveValue(testName)
    await expect(page.locator('input[type="email"]')).toHaveValue(testEmail)
    await expect(page.locator('input[type="password"]')).toHaveValue(testPassword)

    // FIX: Use exact URL pattern with BACKEND_URL (more reliable than wildcard)
    await page.route(`${BACKEND_URL}/auth/signup`, async route => {
      // Return success response matching backend format
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 999,
          user_id: 999,
          email: testEmail,
          full_name: testName,
          message: `✅ User ${testEmail.split('@')[0]} signed up!`
        })
      })
    })

    // Click Create Account and verify signup API was called
    const [signupRequest] = await Promise.all([
      page.waitForRequest(request =>
        request.url().includes('/auth/signup') && request.method() === 'POST'
      ),
      page.locator('button', { hasText: 'Create Account' }).click()
    ])

    // Verify the signup request was made with correct data
    const requestBody = JSON.parse(signupRequest.postData() || '{}')
    expect(requestBody.email).toBe(testEmail)
    expect(requestBody.password).toBe(testPassword)
    expect(requestBody.full_name).toBe(testName)
  })

})
