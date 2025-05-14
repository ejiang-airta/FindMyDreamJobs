// File: frontend/tests/ui/toast-test-helpers.ts
import { Page, expect } from '@playwright/test';

/**
 * Helper functions for testing toast notifications
 */

/**
 * Wait for a toast notification and verify its content
 * 
 * @param page - Playwright page object
 * @param options - Configuration options
 * @param options.text - Text to look for in the toast (can be exact or partial)
 * @param options.exact - Whether to match the exact text or partial content
 * @param options.type - Toast type ('success', 'error', etc.)
 * @param options.timeout - How long to wait for the toast (defaults to 5000ms)
 * @param options.includesEmoji - Whether to check for specific emoji
 * @param options.emoji - Emoji to check for (e.g., '✅' or '❌')
 */
export async function verifyToast(
  page: Page, 
  options: {
    text: string;
    exact?: boolean;
    type?: 'success' | 'error' | 'info' | 'warning';
    timeout?: number;
    includesEmoji?: boolean;
    emoji?: string;
  }
) {
  const { 
    text, 
    exact = false, 
    type, 
    timeout = 5000,
    includesEmoji = false,
    emoji
  } = options;

  // Base selector for toast
  let selector = '.sonner-toast';
  
  // Add type selector if specified
  if (type) {
    selector += `[data-type="${type}"]`;
  }
  
  // Wait for any toast to appear
  const toast = await page.waitForSelector(selector, { timeout });
  
  // Get the text content
  const toastText = await toast.textContent();
  
  // Verify the content based on exact or partial matching
  if (exact) {
    expect(toastText).toBe(text);
  } else {
    expect(toastText).toContain(text);
  }
  
  // Verify emoji if requested
  if (includesEmoji && emoji) {
    expect(toastText).toContain(emoji);
  }
  
  return toast;
}

/**
 * Get all currently visible toast messages
 * 
 * @param page - Playwright page object
 * @returns - Array of toast text contents
 */
// export async function getAllToastMessages(page: Page): Promise<string[]> {
//   const toasts = await page.locator('.sonner-toast').all();
//   const messages = [];
  
//   for (const toast of toasts) {
//     messages.push(await toast.textContent() || '');
//   }
  
//   return messages;
// }

/**
 * Wait for a toast to disappear
 * 
 * @param page - Playwright page object
 * @param text - Text content of toast to wait for disappearance
 * @param timeout - Maximum time to wait in milliseconds
 */
export async function waitForToastToDisappear(
  page: Page,
  text: string,
  timeout = 5000
): Promise<void> {
  await expect(
    page.locator(`.sonner-toast:has-text("${text}")`)
  ).toBeHidden({ timeout });
}

export async function getAllToastMessages(
  page: Page, 
  toastItemSelector: string = '[data-sonner-toaster] > ol > li' // Added second argument with a default value
): Promise<string[]> {
  try {
    // Wait for at least one toast item to be attached to the DOM.
    // If no toasts appear, this will timeout and throw an error,
    // which might be desired behavior or you might want to catch it and return [].
    await page.waitForSelector(toastItemSelector, { state: 'attached', timeout: 5000 });
  } catch (error) {
    // console.warn(`No toast elements found with selector: ${toastItemSelector}`);
    return []; // If no toasts are found after waiting, return an empty array
  }

  const toastElements = await page.locator(toastItemSelector).all();
  const messages: string[] = [];

  for (const toast of toastElements) {
    const textContent = await toast.textContent();
    if (textContent) {
      messages.push(textContent.replace(/\s+/g, ' ').trim());
    }
  }
  return messages;
}