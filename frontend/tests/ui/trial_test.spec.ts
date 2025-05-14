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

test('Test# 15: User can optimize resume', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)

  // Click on Optimize page: 
  await page.getByRole('link', { name: 'Optimize' }).click()
  
  // Verify we're on the Optimize page with "Optimize Resume" text:
  const trackedApplicationsElement = page.locator(':text("🛠 Optimize Resume")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });

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
    timeout: 5000 
  });
})

// ✅ Apply Job
test('Test# 16: User can apply to a job', async ({ page }) => {
  await loginAsTestUser(page, TEST_ENV)

  // Click on Apply page: 
  await page.getByRole('link', { name: 'Apply' }).click()
  
  // Verify we're on the Apply page with "Submit Job Application" text:
  const trackedApplicationsElement = page.locator(':text("📩 Submit Job Application")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });

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
    timeout: 5000 
  });
})



