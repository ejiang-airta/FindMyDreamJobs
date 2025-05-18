// ✅ File: frontend/tests/ui/app_flow.spec.ts
import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { time } from 'console';
import path from 'path';
import fs from 'fs';

const TEST_ENV = process.env.ENV || 'prod'; // Default to production
const BASE_URL = TEST_ENV === 'dev' 
  ? 'http://localhost:3000' 
  : 'https://findmydreamjobs.com'; 

console.log("Base URL: ", BASE_URL)
console.log("Test Environment: ", TEST_ENV)


// Capture start time
const startTime = Date.now();
const formattedTime = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: true, // Ensures AM/PM format
}).format(startTime);

console.log("Test Started at:", formattedTime);

// ✅ Upload Resume
test('Test# 13: User can upload a resume', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV);

  // Debug: Log cookies and URL after login
  console.log("URL after login:", page.url());
  const cookies = await page.context().cookies();
  console.log("Cookies after login:", JSON.stringify(cookies, null, 2));

  // Navigate to the Resume upload page:
  await page.getByRole('link', { name: 'Resume' }).click();
  await page.waitForLoadState('networkidle');
  
  // Debug: Log URL after navigation to Resume page
  console.log("URL at Resume page:", page.url());

  // Verify we're on the Resume page:
  const trackedApplicationsElement = page.locator(':text("📤 Upload Resume")');
  await trackedApplicationsElement.waitFor({ state: 'visible', timeout: 20000 });

  // Generate a random number for the filename:
  const randomNumber = Math.floor(Math.random() * 1000);
  const originalFilePath = path.join(__dirname, './data/example.docx');
  const newFilePath = path.join(__dirname, `./data/example_${randomNumber}.docx`);
  
  // Debug: Check file paths and existence
  console.log("Original file path:", originalFilePath);
  console.log("New file path:", newFilePath);
  console.log("Original file exists:", fs.existsSync(originalFilePath));

  // Copy the original file to a new random filename:
  fs.copyFileSync(originalFilePath, newFilePath);
  console.log("File copied successfully");

  // Select the file input element and upload the new file:
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(newFilePath);
  console.log("File selected for upload");

  // Debug: Check cookies before upload
  const cookiesBeforeUpload = await page.context().cookies();
  console.log("Cookies before upload:", JSON.stringify(cookiesBeforeUpload, null, 2));

  // Click on the Upload Resume button:
  await page.getByRole('button', { name: 'Upload Resume' }).click();
  console.log("Upload button clicked");

  // Capture any error message that appears
  try {
    const errorText = await page.locator('text="User not found in session"').textContent({ timeout: 5000 });
    console.log("Error found:", errorText);
  } catch (e) {
    console.log("No session error found");
  }

  // Wait for the upload to complete:
  await expect(page.locator('body')).toContainText('Resume uploaded successfully!', {
    timeout: 20000
  });
});

// ✅ Analyze Job
test('Test# 14: User can analyze a job description', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)

  // Goes to on Analyze upload page:
  await page.click('text=Analyze')
  // allocate and fill in the job description:
  const jobDescriptionBox =page.locator('textarea[placeholder="Please copy and paste job description here..."]');
  await jobDescriptionBox.fill('Looking for a backend engineer with Python and FastAPI experience.');
  
  // Click the "Analyze Job Description" button;
  await page.getByRole('button', { name: 'Analyze Job Description' }).click();
  
  //verify the toast.success message is appear:
  await expect(page.locator('body')).toContainText('Job description parsed successfully!', { 
    timeout: 20000 
  });
})

// ✅ Optimize Resume
test('Test# 15: User can optimize resume', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)

  // Click on Optimize page: 
  await page.getByRole('link', { name: 'Optimize' }).click()
  
  // Verify we're on the Optimize page with "Optimize Resume" text:
  const trackedApplicationsElement = page.locator(':text("🛠 Optimize Resume")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 20000 });

  // Click on the resume dropdown:
  await page.click('text=Choose your resume'); // Click on the placeholder text
  
  // Wait for dropdown to open and be visible
  await page.waitForSelector('[role="listbox"]', { state: 'visible' });
  
  // Find all resume options and click the first one
  // If the options contain "Resume #" text
  const resumeOptions = page.locator('text=/Resume #/').all();
  const firstResumeOption = (await resumeOptions)[0];
  await firstResumeOption.click();

  // Click on the job dropdown:
  await page.click('text=Choose a job'); // Click on the placeholder text
  
  // Wait for dropdown to open and be visible
  await page.waitForSelector('[role="listbox"]', { state: 'visible' });
  
  // Find all resume options and click the first one
  // If the options contain "Job #" text
  const jobOptions = page.locator('text=/Job #/').all();
  const firstJobOption = (await jobOptions)[0];
  await firstJobOption.click();

  // Click the "Run Optimization" button;
  await page.getByRole('button', { name: '✨ Run Optimization' }).click();
  await expect(page.locator(':text("📝 Optimized Resume Preview")')).toBeVisible({ timeout: 20000 })

  //verify the toast.success message shows up:
  await expect(page.locator('body')).toContainText('Resume optimized successfully!', { 
    timeout: 20000 
  });
})

// ✅ Apply Job
test('Test# 16: User can apply to a job', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)

  // Click on Apply page: 
  await page.getByRole('link', { name: 'Apply' }).click()
  
  // Verify we're on the Apply page with "Submit Job Application" text:
  const trackedApplicationsElement = page.locator(':text("📩 Submit Job Application")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 20000 });

  // Click on the resume dropdown:
  await page.click('text=Select resume'); // Click on the placeholder text
  
  // Wait for dropdown to open and be visible
  await page.waitForSelector('[role="listbox"]', { state: 'visible' });
  
  // Find all resume options and click the first one
  // If the options contain "Resume #" text
  const resumeOptions = page.locator('text=/Resume #/').all();
  const firstResumeOption = (await resumeOptions)[0];
  await firstResumeOption.click();

  // Click on the job dropdown:
  await page.click('text=Select job'); // Click on the placeholder text
  
  // Wait for dropdown to open and be visible
  await page.waitForSelector('[role="listbox"]', { state: 'visible' });
  
  // Find all resume options and click the first one
  // If the options contain "Job #" text
  const jobOptions = page.locator('text=/Job #/').all();
  const firstJobOption = (await jobOptions)[0];
  await firstJobOption.click();

  // enter application link:
  const apply_URL =page.locator('input[placeholder="https://company.com/job/apply"]');
  await apply_URL.fill('https://company.com/job/apply');
  
  // Click the "Submit Application" button;
  await page.getByRole('button', { name: 'Submit Application' }).click();
  
  //verify the toast.success message shows up:
  await expect(page.locator('body')).toContainText('Application submitted!', { 
    timeout: 20000 
  });
})

// ✅ Forgot Password
test('Test# 17: Forgot password page works', async ({ page }) => {
  await page.goto(`${BASE_URL}/login`)

  await page.click('text=Forgot your password?');
  await expect(page.locator(':text("Reset your password")')).toBeVisible({ timeout: 20000 })
  await page.fill('input[type="email"]', 'e_jiang@hotmail.com')
  await page.click('text=Send Reset Link')
  
  // Wait for button state to change
  await expect(page.locator('button:has-text("Sending...")')).toBeVisible();

  // Wait for the success message text to appear anywhere on the page
  await expect(page.locator('body')).toContainText('Password reset email sent! Redirecting to Home', { 
    timeout: 20000 
  });

  // If email sent successfully, we should see home page:
  await expect(page).toHaveURL(`${BASE_URL}`, { timeout: 20000 })
    
  });

// ✅ Unauthorized route guard
test('Test# 18: Unauthorized user is redirected to login page', async ({ page }) => {
  await page.goto(`${BASE_URL}/dashboard`)
  await expect(page).toHaveURL(/.*login/)
  await expect(page.locator(':text("👋 Welcome to FindMyDreamJobs.com! Please sign in or create an account to get started.")')).toBeVisible({ timeout: 20000 })

  // Capture end time
const endTime = Date.now();
const formattedTime = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: true, // Ensures AM/PM format
}).format(endTime);

console.log("Test End at:", formattedTime);

})
