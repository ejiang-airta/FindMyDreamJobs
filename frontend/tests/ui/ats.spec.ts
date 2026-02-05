// File: frontend/tests/ui/ats.spec.ts
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BASE_URL } from './test-config'

test.describe('ATS Score Page', () => {

  test('ats-Test-33-Page-renders-authenticated', async ({ page }) => {
    await loginAsTestUser(page)

    await page.goto(`${BASE_URL}/ats`, { waitUntil: 'domcontentloaded' })
    await expect(page.getByRole('heading', { name: /ATS/ })).toBeVisible({ timeout: 8000 })
  })

  test('ats-Test-34-Validation-error-invalid-resume', async ({ page }) => {
    await loginAsTestUser(page)

    await page.goto(`${BASE_URL}/ats`, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(500)

    // Try submitting with empty or invalid resume ID
    const resumeIdInput = page.locator('input').first()
    if (await resumeIdInput.isVisible()) {
      await resumeIdInput.fill('')
      const checkButton = page.locator('button', { hasText: /check|score|submit/i })
      if (await checkButton.isVisible()) {
        await checkButton.click()
        // Should show validation error
        await expect(page.locator('text=/valid|error|invalid/i')).toBeVisible({ timeout: 5000 })
      }
    }
  })

  test('ats-Test-35-Redirect-unauthenticated', async ({ page }) => {
    await page.goto(`${BASE_URL}/ats`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    // Should show unauthorized message or redirect to login
    await expect(page.locator('body')).toContainText(/Unauthorized|sign in|login/i, {
      timeout: 10000
    })
  })

})
