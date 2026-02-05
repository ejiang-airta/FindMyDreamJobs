// File: frontend/tests/ui/user_isolation.spec.ts
// Test to verify user data isolation - localStorage keys are properly scoped by user_id
import { test, expect } from '@playwright/test'
import { BACKEND_URL } from './test-config'

// Add timestamp to ensure unique emails even if cleanup fails
const timestamp1 = Date.now()
const testUser1 = {
  email: `isolation_user1_${timestamp1}@test.com`,
  password: 'TestPassword123!',
  full_name: 'Isolation User One'
}

const testUser2 = {
  email: `isolation_user2_${timestamp1}@test.com`,
  password: 'TestPassword123!',
  full_name: 'Isolation User Two'
}

const mockJobResults = {
  results: [
    {
      job_id: 'isolation-job-1',
      employer_name: 'Test Company',
      job_title: 'Software Engineer',
      job_city: 'San Francisco',
      job_state: 'CA',
      job_country: 'US',
      job_description: 'We are looking for a Software Engineer with 5 years experience.',
      job_employment_type: 'FULLTIME',
      job_apply_link: 'https://testcompany.com/apply',
      job_location: 'San Francisco, CA',
      job_google_link: 'https://testcompany.com/apply',
      job_posted_at_datetime_utc: new Date().toISOString(),
    },
  ]
}

test.describe('User Data Isolation', () => {

  test('user_isolation-Test-46-All-Jobs-counter-isolated-per-user', async ({ page }) => {
    test.setTimeout(90000) // 90 seconds for complex multi-user test
    let userId1: number | null = null
    let userId2: number | null = null

    try {
      // Register two test users
      await page.goto(`${BACKEND_URL}/docs`)

      // User 1 registration
      const res1 = await page.request.post(`${BACKEND_URL}/auth/signup`, {
        data: testUser1
      })
      expect(res1.ok()).toBeTruthy()
      const userData1 = await res1.json()
      userId1 = userData1.user_id

      // User 2 registration
      const res2 = await page.request.post(`${BACKEND_URL}/auth/signup`, {
        data: testUser2
      })
      expect(res2.ok()).toBeTruthy()
      const userData2 = await res2.json()
      userId2 = userData2.user_id

    // Mock API responses
    await page.route(`**/search-jobs**`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockJobResults),
      })
    })

    await page.route(`**/quick-match-score`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          match_score: 75,
          resume_used: 'Test Resume'
        }),
      })
    })

    // Login as User 1
    await page.goto('/login')
    await page.getByPlaceholder('Email').fill(testUser1.email)
    await page.getByPlaceholder('Password').fill(testUser1.password)
    await page.locator('button', { hasText: 'Sign In' }).click()

    // Wait for login success (redirects to home or dashboard)
    await page.waitForLoadState('networkidle')
    await expect(page.locator('text=Welcome back')).toBeVisible({ timeout: 10000 })

    // User 1 searches for jobs
    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.getByPlaceholder('Job title or keywords').fill('Software Engineer')
    await page.getByRole('button', { name: 'Search Jobs' }).click()
    await expect(page.getByRole('heading', { name: 'Software Engineer' })).toBeVisible({ timeout: 10000 })

    // Verify User 1 sees the job AND "All Jobs (1)"
    await expect(page.locator('text=Test Company')).toBeVisible()
    await expect(page.locator('text=All Jobs (1)')).toBeVisible({ timeout: 5000 })

    // Logout
    await page.getByRole('button', { name: /sign out/i }).click()
    await page.waitForURL('**/login', { timeout: 10000 })

    // Login as User 2
    await page.getByPlaceholder('Email').fill(testUser2.email)
    await page.getByPlaceholder('Password').fill(testUser2.password)
    await page.locator('button', { hasText: 'Sign In' }).click()

    // Wait for login success
    await page.waitForLoadState('networkidle')
    await expect(page.locator('text=Welcome back')).toBeVisible({ timeout: 10000 })

    // Navigate to Jobs page as User 2
    await page.getByRole('link', { name: 'Jobs' }).click()

    // User 2 should see ALL COUNTERS at (0) - NOT User 1's data
    await expect(page.locator('text=All Jobs (0)')).toBeVisible({ timeout: 5000 })
    await expect(page.locator('text=Saved (0)')).toBeVisible({ timeout: 5000 })
    await expect(page.locator('text=Analyzed (0)')).toBeVisible({ timeout: 5000 })
    await expect(page.locator('text=Applied (0)')).toBeVisible({ timeout: 5000 })
    } finally {
      // Cleanup: delete both users
      if (userId1) {
        try {
          await page.request.post(`${BACKEND_URL}/delete-user`, {
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({ user_id: userId1 }),
            timeout: 5000
          })
        } catch (e) {
          console.log(`Cleanup failed for user ${userId1}:`, e)
        }
      }
      if (userId2) {
        try {
          await page.request.post(`${BACKEND_URL}/delete-user`, {
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({ user_id: userId2 }),
            timeout: 5000
          })
        } catch (e) {
          console.log(`Cleanup failed for user ${userId2}:`, e)
        }
      }
    }
  })
})
