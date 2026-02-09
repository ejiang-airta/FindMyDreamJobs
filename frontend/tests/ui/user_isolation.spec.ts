// File: frontend/tests/ui/user_isolation.spec.ts
// Test to verify user data isolation - localStorage keys are properly scoped by user_id
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BASE_URL, BACKEND_URL } from './test-config'

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
  ],
}

test.describe('User Isolation', () => {
  test('Test# 46: Jobs counter isolation', async ({ page }) => {
    test.setTimeout(90000) // 90 seconds for complex multi-user test

    // Mock job search API
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
          resume_used: 'Test Resume',
        }),
      })
    })

    const counter = page.locator('text=/All Jobs \\(\\d+\\)/')

    // User 1: Login with existing test user
    await loginAsTestUser(page)

    // Navigate to Jobs page and search
    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.waitForLoadState('networkidle')

    await page.getByPlaceholder('Job title or keywords').fill('Software Engineer')
    await page.getByRole('button', { name: 'Search Jobs' }).click()
    await page.waitForLoadState('networkidle')

    // ✅ Fix 2: wait for counter to update to > 0
    await expect(counter).toContainText(/All Jobs \([1-9]\d*\)/)

    // Get User 1's job counter (should be > 0 after search)
    const user1CounterText = await counter.textContent()

    // ✅ Fix 1: correct digit regex
    const user1Count = parseInt(user1CounterText?.match(/\d+/)?.[0] || '0', 10)
    expect(user1Count).toBeGreaterThan(0)

    // Logout User 1
    await page.getByRole('button', { name: 'Sign Out' }).click()
    await page.waitForLoadState('networkidle')

    // User 2: Create new user and login
    const timestamp = Date.now()
    const user2Email = `isolation_user2_${timestamp}@test.com`
    const user2Name = `Isolation User Two ${timestamp}`

    // Navigate to signup
    await page.goto(`${BASE_URL}/signup`)
    await page.fill('input[type="text"]', user2Name)
    await page.fill('input[type="email"]', user2Email)
    await page.fill('input[type="password"]', 'TestPassword123!')

    // Mock signup API
    await page.route(`${BACKEND_URL}/auth/signup`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 998,
          user_id: 998,
          email: user2Email,
          full_name: user2Name,
          message: 'User created successfully',
        }),
      })
    })

    await page.locator('button', { hasText: 'Create Account' }).click()
    await page.waitForLoadState('networkidle')

    // Navigate to Jobs page as User 2
    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.waitForLoadState('networkidle')

    // ✅ Fix 2 (optional but consistent): wait for counter to show 0 for new user
    await expect(counter).toContainText(/All Jobs \(0\)/)

    // Get User 2's job counter (should be 0, isolated from User 1)
    const user2CounterText = await counter.textContent()

    // ✅ Fix 1: correct digit regex
    const user2Count = parseInt(user2CounterText?.match(/\d+/)?.[0] || '0', 10)

    // Verify isolation - User 2 should have 0 jobs (different from User 1)
    expect(user2Count).toBe(0)
    expect(user1Count).not.toBe(user2Count)
  })

})