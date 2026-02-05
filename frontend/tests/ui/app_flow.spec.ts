// File: frontend/tests/ui/app_flow.spec.ts
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BASE_URL } from './test-config'
import path from 'path'
import fs from 'fs'

test.describe('Core Application Flows', () => {

  test('app_flow-Test-13-User-can-upload-resume', async ({ page }) => {
    await loginAsTestUser(page)

    // Navigate to the Resume upload page
    await page.getByRole('link', { name: 'Resume' }).click()
    // Wait for the specific heading to ensure the page logic is loaded
    await expect(page.getByRole('heading', { name: /Upload Resume/ })).toBeVisible({ timeout: 20000 })

    // Copy example file to a temp name to avoid duplicate-name errors
    const randomNumber = Math.floor(Math.random() * 10000)
    const originalFilePath = path.join(__dirname, './data/example.docx')
    const newFilePath = path.join(__dirname, `./data/example_${randomNumber}.docx`)
    fs.copyFileSync(originalFilePath, newFilePath)

    try {
      // FIX: Use setInputFiles directly (more reliable than fileChooser event)
      const fileInput = page.locator('input[type="file"]')
      await fileInput.setInputFiles(newFilePath)

      // Wait for the button to be enabled (file should be loaded)
      const uploadButton = page.getByRole('button', { name: 'Upload Resume' })
      await expect(uploadButton).toBeEnabled({ timeout: 10000 })
      await uploadButton.click()

      // Wait for success message - try multiple possible selectors
      // First try the body text approach (fallback)
      await expect(page.locator('body')).toContainText(/uploaded successfully|Resume uploaded/i, { timeout: 20000 })
    } finally {
      // Clean up the temporary file
      if (fs.existsSync(newFilePath)) {
        fs.unlinkSync(newFilePath)
      }
    }
  })

  test('app_flow-Test-14-Analyze-job-description', async ({ page }) => {
    await loginAsTestUser(page)

    await page.click('text=Analyze')
    const jobDescriptionBox = page.locator('textarea[placeholder="Please copy and paste job description here..."]')
    await jobDescriptionBox.fill('Looking for a backend engineer with Python and FastAPI experience.')

    await page.getByRole('button', { name: 'Analyze Job Description' }).click()

    await expect(page.locator('body')).toContainText('Job description parsed successfully!', {
      timeout: 20000
    })
  })

  test('app_flow-Test-15-Optimize-resume', async ({ page }) => {
    await loginAsTestUser(page)

    await page.getByRole('link', { name: 'Optimize' }).click()
    await expect(page.getByRole('heading', { name: /Optimize Resume/ })).toBeVisible({ timeout: 20000 })

    // --- Select a Resume ---
    await page.click('text=Choose your resume')
    
    // Use a locator that specifically looks for the option inside the visible listbox
    const resumeOption = page.locator('[role="listbox"] >> text=/Resume #/').first()
    
    // Playwright will automatically wait/retry for this to be visible and actionable
    await resumeOption.click()

    // --- Select a Job ---
    await page.click('text=Choose a job')
    
    // Scope the search to the listbox to avoid clicking background elements
    const jobOption = page.locator('[role="listbox"] >> text=/Job #/').first()
    await jobOption.click()

    // --- Run optimization ---
    const runBtn = page.getByRole('button', { name: 'Run Optimization' })
    await expect(runBtn).toBeEnabled()
    await runBtn.click()
    
    await expect(page.getByRole('heading', { name: /Optimized Resume Preview/ })).toBeVisible({ timeout: 20000 })
    await expect(page.locator('body')).toContainText('Resume optimized successfully!', {
      timeout: 20000
    })
  })

  test('app_flow-Test-16-Apply-to-job', async ({ page }) => {
    await loginAsTestUser(page)

    await page.getByRole('link', { name: 'Apply' }).click()
    await expect(page.getByRole('heading', { name: /Submit Job Application/ })).toBeVisible({ timeout: 20000 })

    // Select resume
    await page.waitForTimeout(500)
    await page.click('text=Select resume')
    await page.waitForSelector('[role="listbox"]', { state: 'visible' })
    const firstResumeOption = (await page.locator('text=/Resume #/').all())[0]
    await firstResumeOption.click()

    // Select job
    await page.click('text=Select job')
    await page.waitForSelector('[role="listbox"]', { state: 'visible' })
    const firstJobOption = (await page.locator('text=/Job #/').all())[0]
    await firstJobOption.click()

    // Enter application link
    await page.locator('input[placeholder="https://company.com/job/apply"]').fill('https://company.com/job/apply')

    // Submit
    await page.getByRole('button', { name: 'Submit Application' }).click()
    await expect(page.locator('body')).toContainText('Application submitted!', {
      timeout: 20000
    })
  })

  test('app_flow-Test-17-Forgot-password-flow', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`)
    await page.click('text=Forgot your password?')
    await expect(page.locator(':text("Reset your password")')).toBeVisible({ timeout: 20000 })

    await page.fill('input[type="email"]', 'e_jiang@hotmail.com')
    await page.waitForTimeout(500)
    await page.click('text=Send Reset Link')

    // Wait for button state change
    await expect(page.locator('button:has-text("Sending...")')).toBeVisible()

    // Wait for success message and redirect
    await expect(page.locator('body')).toContainText('Password reset email sent! Redirecting to Home', {
      timeout: 20000
    })
    await expect(page).toHaveURL(`${BASE_URL}`, { timeout: 20000 })
  })

  test('app_flow-Test-18-Unauthorized-redirect', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`)
    await expect(page.locator('body')).toContainText('Please sign in or create an account to get started', {
      timeout: 20000
    })
    await expect(page).toHaveURL(/.*login/)
  })

})
