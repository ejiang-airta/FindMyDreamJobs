// File: /frontend/tests/ui/toast-verification.spec.ts

import { test, expect } from '@playwright/test';
import { verifyToast, getAllToastMessages, waitForToastToDisappear } from './toast-test-helpers'; // You'll likely need to update these helpers too
import { loginAsTestUser } from './helpers'

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

test.describe('Toast Verification Examples', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/login/forgot-password`);
  });

  test('should verify exact toast message with emoji', async ({ page }) => {
    // Mock the success response
    await page.route(`**/auth/request-password-reset`, route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Success' }), // Or ensure this is the exact response triggering the toast
      });
    });
    
    // Fill email and submit form
    await page.fill('input[type="email"]', 'e_jiang@hotmail.com');  
    await page.click('button:has-text("Send Reset Link")');
    
    // --- UPDATED APPROACH 1: Direct verification with expect ---
    // Option A: If [data-sonner-toaster] IS the toast element itself or a direct, unique wrapper
    // const toastSelector = '[data-sonner-toaster]'; 
    // Option B: If toasts are list items within the [data-sonner-toaster] container
    // This is a common pattern for Sonner: the toaster is an <ol> and toasts are <li>
    const toastSelector = '[data-sonner-toaster] > ol > li'; 
    // Option C: A more general selector that worked in your debug log for a single toast:
    // const toastSelector = '[aria-live="polite"]'; 
    // Let's go with Option B as it's specific to Sonner's typical structure,
    // but you can test A or C if B doesn't work or captures too much.

    // Wait for the toast to appear (it might be an li element within the toaster)
    // We'll look for an element that IS a toast and contains part of the expected text to make it more robust
    const toast = await page.waitForSelector(
      // This selector finds a list item inside the sonner toaster
      // that contains the specific text.
      `${toastSelector}:has-text("Password reset email sent!")`, 
      { timeout: 5000 }
    );
    const fullText = await toast.textContent();
    // Normalize whitespace and newlines that might come from textContent() across different elements
    const normalizedText = fullText?.replace(/\s+/g, ' ').trim();
    expect(normalizedText).toBe('✅ Password reset email sent! Redirecting to Home...');
    
    // --- You will need to update your helper functions verifyToast, getAllToastMessages etc. ---
    // --- to use a similar selector strategy. ---

    // For example, verifyToast might now internally use:
    // const baseSelector = '[data-sonner-toaster] > ol > li';
    // And then add :has-text or other conditions.

    // APPROACH 2 (assuming verifyToast is updated)
    await verifyToast(page, {
      text: '✅ Password reset email sent! Redirecting to Home...',
      exact: true,
      type: 'success' // 'type' might need to check for data-toast-type attributes if Sonner uses them
    });
    
    // APPROACH 3 (assuming verifyToast is updated)
    await verifyToast(page, {
      text: 'Password reset email sent!',
      exact: false
    });
    
    // APPROACH 4 (assuming verifyToast is updated)
    await verifyToast(page, {
      text: 'Password reset email sent!',
      includesEmoji: true,
      emoji: '✅'
    });
  });

  // ... (rest of your tests)
  
  test('should handle toast with unusual structure', async ({ page }) => {
    await page.route(`**/auth/request-password-reset`, route => {
      route.fulfill({ status: 200, body: JSON.stringify({}) });
    });
    
    await page.fill('input[type="email"]', 'e_jiang@hotmail.com');
    await page.click('button:has-text("Send Reset Link")');
    
    // Wait for a toast to appear (adjust selector as per findings)
    // Example using the structure seen in Sonner: <ol data-sonner-toaster><li>toast content</li></ol>
    const toastContainerSelector = '[data-sonner-toaster]';
    const toastItemSelector = `${toastContainerSelector} > ol > li`; // Individual toast

    await page.waitForSelector(toastItemSelector, { timeout: 5000 });
    
    // Method 1: Check each part separately
    // Sonner often uses specific data attributes for title, description, icon
    // e.g., [data-title], [data-description], [data-icon] within the 'li'
    const iconText = await page.locator(`${toastItemSelector} [data-icon], ${toastItemSelector} [role="img"]`).textContent(); // Adjust if Sonner has a specific icon selector
    expect(iconText).toContain('✅');
    
    // For Sonner, the message might be directly in the <li> or in a child <div> or <div data-title>
    const messageText = await page.locator(`${toastItemSelector}`).textContent(); // Or a more specific child
    expect(messageText).toContain('Password reset email sent!');
    expect(messageText).toContain('Redirecting to Home...'); // Assuming description is part of the main text node or a sibling
    
    // Method 2: Use regular expressions for flexible matching on the toast item
    const allTextInToastItem = await page.locator(toastItemSelector).textContent();
    const normalizedAllText = allTextInToastItem?.replace(/\s+/g, ' ').trim();
    expect(normalizedAllText).toMatch(/✅ Password reset email sent! Redirecting to Home/);
  });
  
  test('should verify toast is dismissed after timeout', async ({ page }) => {
    await page.route(`**/auth/request-password-reset`, route => {
      route.fulfill({ status: 200, body: JSON.stringify({}) });
    });
    
    await page.fill('input[type="email"]', 'test@example.com');
    await page.click('button:has-text("Send Reset Link")');
    
    // First verify toast appears (assuming verifyToast is updated)
    await verifyToast(page, { text: 'Password reset email sent!' });
    
    // Then verify it disappears (your toast duration is set to 4000ms)
    // waitForToastToDisappear will also need to know the correct selector or how to identify toasts
    await waitForToastToDisappear(page, 'Password reset email sent!', 5000);
  });
  
  test('should capture all toast messages', async ({ page }) => {
    await page.route(`**/auth/request-password-reset`, route => {
      route.fulfill({ status: 200, body: JSON.stringify({}) });
    });
    await expect(page.locator(':text("Reset your password")')).toBeVisible({ timeout: 5000 })
    await page.fill('input[type="email"]', 'test@example.com');
    await page.click('button:has-text("Send Reset Link")');
    
    // Wait for the toaster container to have at least one toast
    await page.waitForSelector('[data-sonner-toaster] > ol > li', { timeout: 5000 });
    
    // Get all toast messages (getAllToastMessages needs update)
    const messages = await getAllToastMessages(page, '[data-sonner-toaster] > ol > li'); // Pass the correct selector
    
    expect(messages.length).toBeGreaterThan(0);
    
    const hasExpectedMessage = messages.some(msg => 
      msg.includes('Password reset email sent!')
    );
    expect(hasExpectedMessage).toBeTruthy();
  });
});