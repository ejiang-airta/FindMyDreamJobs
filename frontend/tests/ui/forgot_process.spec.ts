import { test, expect } from '@playwright/test'
import { loginAsTestUser } from './helpers'
import { BASE_URL } from './test-config'
import path from 'path';
import fs from 'fs';

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


test('upload resume through selection box', async ({ page }) => {
  
  await loginAsTestUser(page)  

  /// Click on Match button
  await page.getByRole('link', { name: 'Resume' }).click()
  
  // Verify we're on the Resume page:
  const trackedApplicationsElement = page.locator(':text("📤 Upload Resume")');
  await trackedApplicationsElement.waitFor({ state: 'visible',  timeout: 8000 });
  // Navigate to the upload resume page
  //await page.goto('/upload'); 
  
  // Prepare a file to upload - create a path to a test file in your project
  const testFilePath = path.join(__dirname, './data/example_1.docx'); // Adjust path as needed
  
  // This is the key part - we set up the file input without clicking the button that opens the dialog
  // Instead of clicking the selection box that would open a system dialog, we use page.setInputFiles()
  // First, get the file input element (might be hidden)
  const fileInput = page.locator('input[type="file"]');
  
  // If the file input is hidden (common in styled upload components):
  await fileInput.setInputFiles(testFilePath);

  // Click on the Upload Resume button:
  //await page.click('text=Upload Resume')
  //await page.getByText('Upload Resume').click();
  await page.getByRole('button', { name: 'Upload Resume' }).click();
  
  // Wait for the upload to complete - look for confirmation text or changes in UI
  await expect(page.locator('body')).toContainText('Resume uploaded successfully!', {
    timeout: 10000
  });
});