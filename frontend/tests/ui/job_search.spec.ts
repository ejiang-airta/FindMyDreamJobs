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

  test('Test# 23: User can search for jobs and see results', async ({ page }) => {
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

  test('Test# 24: Search with no results shows zero count', async ({ page }) => {
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

  test('Test# 25: Search handles API errors gracefully', async ({ page }) => {
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

})
