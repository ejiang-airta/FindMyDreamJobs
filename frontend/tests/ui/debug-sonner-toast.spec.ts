import { test, expect } from '@playwright/test';

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

test('Debug sonner toast structure', async ({ page }) => {
  // Navigate to the forgot password page
  await page.goto(`${BASE_URL}/login/forgot-password`);
  
  // This will help debug DOM structure
  await page.evaluate(() => {
    // Add debugging style to highlight toast container when it appears
    const style = document.createElement('style');
    style.innerHTML = `
      [id*="sonner"], [class*="sonner"], [data-sonner], 
      [id*="toast"], [class*="toast"], [data-toast],
      [id*="notification"], [class*="notification"] {
        outline: 3px solid red !important;
      }
    `;
    document.head.appendChild(style);
  });
  
  // Enable request interception
  await page.route(`**/auth/request-password-reset`, route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ message: 'Success' }),
    });
  });
  
  // Fill in the email
  await page.fill('input[type="email"]', 'test@example.com');
  
  // Start tracing before clicking to analyze DOM changes
  await page.evaluate(() => {
    console.log('DOM before toast:', document.body.innerHTML);
    
    // Setup mutation observer to detect toast being added
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.addedNodes.length) {
          console.log('Added nodes:', mutation.addedNodes);
          for (const node of mutation.addedNodes) {
            if (node.nodeType === 1) { // Element node
              const elem = node;
              if (elem.textContent && elem.textContent.includes('Password reset')) {
                console.log('Potential toast found:', elem.tagName, 
                  'Classes:', elem.className,
                  'ID:', elem.id,
                  'HTML:', elem.outerHTML);
              }
            }
          }
        }
      }
    });
    
    // Observe the entire document
    observer.observe(document.body, { 
      childList: true, 
      subtree: true,
      attributes: true,
      characterData: true
    });
    
    window._toastObserver = observer; // Save reference to prevent garbage collection
  });
  
  // Click the send reset link button
  await page.click('button:has-text("Send Reset Link")');
  
  // Wait a moment for potential toasts to appear
  await page.waitForTimeout(1000);
  
  // Debug: Take screenshot to see if toast is visible
  await page.screenshot({ path: 'debug-toast.png' });
  
  // Try various potential selectors
  const potentialSelectors = [
    // Standard Sonner selectors
    '[data-sonner-toaster]',
    '.sonner-toaster',
    '.sonner-toast-container',
    '.sonner-toast',
    
    // Common toast library selectors
    '.toast',
    '.Toastify__toast',
    '.notification',
    '.toast-notification',
    
    // Attribute selectors
    '[role="alert"]',
    '[aria-live="polite"]',
    
    // Text content selectors
    'div:has-text("Password reset email sent!")',
    'div:has-text("Redirecting to Home")',
    'div:has-text("✅")',
  ];
  
  // Try all selectors
  console.log('Checking potential toast selectors:');
  for (const selector of potentialSelectors) {
    const count = await page.locator(selector).count();
    console.log(`Selector "${selector}": ${count} elements found`);
    
    if (count > 0) {
      console.log('Found elements with selector:', selector);
      const elements = await page.locator(selector).all();
      for (let i = 0; i < elements.length; i++) {
        const text = await elements[i].textContent();
        console.log(`  Element ${i+1} text:`, text);
      }
    }
  }
  
  // Check toast content in the DOM
  const bodyText = await page.locator('body').textContent();
  if (bodyText?.includes('Password reset email sent!')) {
    console.log('Toast text found in body but selector might be wrong');
  }
  
  // Check if anything in portal containers (where toasts often live)
  const portalElements = await page.locator('#__next > div, body > div:not(#__next)').all();
  console.log(`Found ${portalElements.length} potential portal containers`);
  
  for (let i = 0; i < portalElements.length; i++) {
    const text = await portalElements[i].textContent();
    if (text?.includes('Password reset') || text?.includes('✅')) {
      console.log(`Portal element ${i+1} contains toast text:`, text);
      console.log('Portal HTML:', await portalElements[i].evaluate(el => el.outerHTML));
    }
  }
  
  // Extract DOM information to help identify the toast
  const domInfo = await page.evaluate(() => {
    return {
      bodyHTML: document.body.innerHTML,
      toastText: Array.from(document.querySelectorAll('*'))
        .filter(el => el.textContent?.includes('Password reset email sent!'))
        .map(el => ({
          tagName: el.tagName,
          className: el.className,
          id: el.id,
          text: el.textContent?.trim()
        }))
    };
  });
  
  console.log('Elements containing toast text:', domInfo.toastText);
});