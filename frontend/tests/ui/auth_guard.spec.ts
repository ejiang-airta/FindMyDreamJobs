// File: frontend/tests/ui/auth_guard.spec.ts
// Verifies that protected routes redirect unauthenticated users to login
import { test, expect } from '@playwright/test'
import { BASE_URL } from './test-config'

const protectedRoutes = [
  '/dashboard',
  '/upload',
  '/analyze',
  '/match',
  '/optimize',
  '/apply',
  '/applications',
  '/stats',
  '/wizard',
  '/matches',
]

// Test# 36-45: Auth guard tests for all protected routes
test.describe('Auth Guards', () => {

  for (const [index, route] of protectedRoutes.entries()) {
    test(`Test# ${36 + index}: No access to ${route} re-login`, async ({ page }) => {
      await page.goto(`${BASE_URL}${route}`, { waitUntil: 'domcontentloaded', timeout: 60000 })

      // Should redirect to login or show sign-in message
      await expect(page.locator('body')).toContainText(/sign in|login|create an account/i, {
        timeout: 15000
      })
    })
  }

})
