// File: frontend/tests/ui/login.spec.ts

import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'


const TEST_ENV = process.env.ENV || 'prod'; // Default to production
const BASE_URL = TEST_ENV === 'dev' 
  ? 'http://localhost:3000' 
  : 'https://findmydreamjobs.com'; 

console.log("Base URL: ", BASE_URL)
console.log("Test Environment: ", TEST_ENV)

// Capture start time
const startTime = Date.now();
console.log("Test Started at: ", startTime)

test(`Test #1: User can visit login page and see email/password fields in ${TEST_ENV} environment`, async ({ page }) => {
  await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 60000 }) // Wait up to 60 seconds for page load  

  // Check that email and password input fields exist
  const emailInput = page.locator('input[type="email"]')
  const passwordInput = page.locator('input[type="password"]')
  const loginButton = page.locator('button', { hasText: 'Sign In' })

  await expect(emailInput).toBeVisible()
  await expect(passwordInput).toBeVisible()
  await expect(loginButton).toBeVisible()
})

test('Test #2: Login fails with incorrect credentials (via alert dialog)', async ({ page }) => {
// Check that a toast or error appears
  page.on('dialog', async dialog => {
    expect(dialog.message()).toContain('Please enter both email and password.')
    await dialog.dismiss()
  })

  await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 60000 }) // Wait up to 60 seconds for page load
  await page.fill('input[type="email"]', 'fakeuser@example.com')
  await page.fill('input[type="password"]', 'wrongpassword')
  await page.locator('button', { hasText: 'Sign In' }).click()
})
test('Test #3: Login succeeds with correct credentials and lands on home page', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)
  //await page.getByRole('button', { name: 'Dashboard' }).click()

  // Wait for redirect and assert user’s name is visible
  await expect(page.getByText('Welcome back, test user1!')).toBeVisible({ timeout: 5000 })
  
})

test('Test #4: Navigate to Dashboard and verify Tracked Applications is present', async ({ page }) => {
  // Go to the initial page (replace with your page URL)
  await loginAsTestUser(page, TEST_ENV)

  // Locate and click the Dashboard button in the navigation bar.
  // We'll be specific to target the text within the navigation element.
  const dashboardNavLink = page.locator('nav.bg-white :text("Dashboard")');
  await expect(dashboardNavLink).toBeVisible(); // Optional: Assert the link is visible before clicking
  await dashboardNavLink.click();

  // Confirm we’re on the dashboard
  await expect(page).toHaveURL(`${BASE_URL}/dashboard`);

  // After clicking, you should be on the dashboard page.
  // Now, verify that the "Tracked Applications" text exists on the new page.
  const trackedApplicationsElement = page.locator(':text("📋 Tracked Applications")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });  
});

test('Test #5: User can log in and access Analyze page', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  // Click on Analyze button
  await page.getByRole('link', { name: 'Analyze' }).click()
  
  // Verify we're on the Analyze page with "Analyze Job Description" text:
  const trackedApplicationsElement = page.locator(':text("📄 Analyze Job Description")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #6: Access Match page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  /// Click on Match button
  await page.getByRole('link', { name: 'Match' }).click()
  
//   // Verify we're on the Match page with "Match Score" text:
  const trackedApplicationsElement = page.locator(':text("📊 Match Score")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #7: Access Optimize page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  // Click on Optimize button
  await page.getByRole('link', { name: 'Optimize' }).click()
  
  // Verify we're on the Optimize page with "Optimize Resume" text:
  const trackedApplicationsElement = page.locator(':text("🛠 Optimize Resume")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #8: Access Apply page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  /// Click on Apply button
  await page.getByRole('link', { name: 'Apply' }).click()
  
//   // Verify we're on the Apply page with "📩 Submit Job Application" text:
  const trackedApplicationsElement = page.locator(':text("📩 Submit Job Application")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #9: Access Applications page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  /// Click on Applications button
  await page.getByRole('link', { name: 'Applications' }).click()
  
//   // Verify we're on the Applications page with "📌 Your Job Applications" text:
  const trackedApplicationsElement = page.locator(':text("📌 Your Job Applications")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #10: Access Stats page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  /// Click on Stats button
  await page.getByRole('link', { name: 'Stats' }).click()
  
//   // Verify we're on the Stats page with "📊 Application Stats" text:
  const trackedApplicationsElement = page.locator(':text("📊 Application Stats")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #11: Access Wizard page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  /// Click on Wizard button
  await page.getByRole('link', { name: 'Wizard' }).click()
  
//   // Verify we're on the Wizard page with "🚀 Smart Job Application Wizard" text:
  const trackedApplicationsElement = page.locator(':text("🚀 Smart Job Application Wizard")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
});

test('Test #12: Switch to Home page after login', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)  

  // Click on Analuze button
  await page.getByRole('link', { name: 'Analyze' }).click()
  // Click on Home button
  await page.getByRole('link', { name: 'Home' }).click()
    
  
    // Wait for redirect and assert user’s name is visible
  await expect(page.getByText('Welcome back, test user1!')).toBeVisible({ timeout: 5000 })

  // Capture End time
  const endTime = Date.now();
  console.log("Test Completed at: ", endTime)

  // Capture duration time
  const duration = (endTime - startTime) / 1000; // Convert to seconds
  console.log("Total Duration for this round: ", duration, " seconds")
});

