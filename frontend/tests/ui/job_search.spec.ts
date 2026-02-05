// File: frontend/tests/ui/job_search.spec.ts
// Uses Playwright's page.route() for API interception (NOT MSW, which doesn't work in E2E)
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BACKEND_URL } from './test-config'

const mockJobResults = {
  results: [
    {
      job_id: 'test-job-1',
      employer_name: 'Test Company',
      job_title: 'QA Engineer',
      job_city: 'San Francisco',
      job_state: 'CA',
      job_country: 'US',
      job_description: 'We are looking for a QA Engineer with automation experience.',
      job_employment_type: 'FULLTIME',
      job_apply_link: 'https://testcompany.com/apply',
      job_min_salary: 80000,
      job_max_salary: 120000,
      job_salary_currency: 'USD',
      job_salary_period: 'YEAR',
    },
    {
      job_id: 'test-job-2',
      employer_name: 'Another Corp',
      job_title: 'Software Developer',
      job_city: 'New York',
      job_state: 'NY',
      job_country: 'US',
      job_description: 'Full-stack developer needed for a growing team.',
      job_employment_type: 'FULLTIME',
      job_apply_link: 'https://anothercorp.com/apply',
    },
  ]
}

test.describe('Job Search', () => {

  test('job_search-Test-23-Search-and-see-results', async ({ page }) => {
    await loginAsTestUser(page)

    // Intercept the search-jobs API call with mock data
    await page.route(`**/search-jobs**`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockJobResults),
      })
    })

    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.getByPlaceholder('Job title or keywords').fill('QA Engineer')
    await page.getByRole('button', { name: 'Search Jobs' }).click()

    // Wait for mocked results to appear — use heading to avoid strict mode (title + description both contain text)
    await expect(page.locator('text=Test Company')).toBeVisible({ timeout: 10000 })
    await expect(page.getByRole('heading', { name: 'QA Engineer' })).toBeVisible()
    await expect(page.locator('text=Another Corp')).toBeVisible()
  })

  test('job_search-Test-24-Search-no-results', async ({ page }) => {
    await loginAsTestUser(page)

    // Intercept with empty results
    await page.route(`**/search-jobs**`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ results: [] }),
      })
    })

    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.getByPlaceholder('Job title or keywords').fill('NonexistentJob')
    await page.getByRole('button', { name: 'Search Jobs' }).click()

    // The page shows "Showing 0 jobs" when no results
    await expect(page.locator('text=Showing 0 jobs')).toBeVisible({ timeout: 10000 })
  })

  test('job_search-Test-25-API-error-handling', async ({ page }) => {
    await loginAsTestUser(page)

    // Intercept with error response
    await page.route(`**/search-jobs**`, route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' }),
      })
    })

    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.getByPlaceholder('Job title or keywords').fill('ErrorTest')
    await page.getByRole('button', { name: 'Search Jobs' }).click()

    // The page should not crash — verify it's still functional
    await page.waitForTimeout(3000)
    await expect(page.getByPlaceholder('Job title or keywords')).toBeVisible()
  })

  test('job_search-Test-26-Analyze-navigates-with-JD', async ({ page }) => {
    await loginAsTestUser(page)

    // Intercept the search-jobs API call with mock data
    await page.route(`**/search-jobs**`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockJobResults),
      })
    })

    // Navigate to jobs page and search
    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.getByPlaceholder('Job title or keywords').fill('QA Engineer')
    await page.getByRole('button', { name: 'Search Jobs' }).click()

    // Wait for results
    await expect(page.getByRole('heading', { name: 'QA Engineer' })).toBeVisible({ timeout: 10000 })

    // Click the Analyze button on the first job card
    await page.getByRole('button', { name: 'Analyze' }).first().click()

    // Should navigate to /analyze page
    await expect(page).toHaveURL(/.*\/analyze/, { timeout: 5000 })

    // The job description should be pre-filled in the textarea
    const textarea = page.getByPlaceholder('Please copy and paste job description here...')
    await expect(textarea).toBeVisible()

    // Check that the textarea contains the job description
    const textareaValue = await textarea.inputValue()
    expect(textareaValue).toContain('We are looking for a QA Engineer')
  })

  test('job_search-Test-27-Match-scores-color-coding', async ({ page }) => {
    await loginAsTestUser(page)

    // Intercept the search-jobs API call
    await page.route(`**/search-jobs**`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockJobResults),
      })
    })

    // Intercept the quick-match-score API calls with different scores
    let callCount = 0
    await page.route(`**/quick-match-score`, route => {
      callCount++
      // Return different scores for each job to test color coding
      const score = callCount === 1 ? 85 : 65 // First job: 85% (green), second: 65% (yellow)
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          match_score: score,
          resume_used: 'Test Resume'
        }),
      })
    })

    // Navigate to jobs page and search
    await page.getByRole('link', { name: 'Jobs' }).click()
    await page.getByPlaceholder('Job title or keywords').fill('QA Engineer')
    await page.getByRole('button', { name: 'Search Jobs' }).click()

    // Wait for results
    await expect(page.getByRole('heading', { name: 'QA Engineer' })).toBeVisible({ timeout: 10000 })

    // Wait for match scores to be calculated and displayed
    await expect(page.locator('text=85% Match')).toBeVisible({ timeout: 8000 })
    await expect(page.locator('text=65% Match')).toBeVisible({ timeout: 8000 })

    // Verify color coding by checking badge classes
    // Green badge for 85% (≥80%)
    const greenBadge = page.locator('.bg-green-100').filter({ hasText: '85% Match' })
    await expect(greenBadge).toBeVisible()

    // Yellow badge for 65% (≥60%, <80%)
    const yellowBadge = page.locator('.bg-yellow-100').filter({ hasText: '65% Match' })
    await expect(yellowBadge).toBeVisible()
  })

})
