// File: frontend/tests/ui/signup.spec.ts
import { test, expect } from '@playwright/test'
import { BASE_URL } from './test-config'

test.describe('Signup Page', () => {

  test('Test# 26: Signup page renders with all form fields', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    await expect(page.getByRole('heading', { name: /Create New Account/ })).toBeVisible()
    await expect(page.locator('input[type="text"]')).toBeVisible()  // Full name
    await expect(page.locator('input[type="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
    await expect(page.locator('button', { hasText: 'Sign Up' })).toBeVisible()
  })

  test('Test# 27: Signup page has link to login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    const signInLink = page.locator('a', { hasText: 'Sign In' })
    await expect(signInLink).toBeVisible()
    await signInLink.click()
    await expect(page).toHaveURL(/.*login/)
  })

  test('Test# 28: Signup with missing fields shows alert', async ({ page }) => {
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('Please enter all fields.')
      await dialog.dismiss()
    })

    await page.goto(`${BASE_URL}/signup`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    // Only fill email, leave name and password empty
    await page.fill('input[type="email"]', 'test@example.com')
    await page.locator('button', { hasText: 'Sign Up' }).click()
  })

})
