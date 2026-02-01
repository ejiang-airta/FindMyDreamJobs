// ✅ File: frontend/playwright.config.ts
import { defineConfig, devices } from '@playwright/test'
import { BASE_URL } from './tests/ui/test-config'

export default defineConfig({
  testDir: './tests/ui',
    /* Add this reporter section. 
     'open': 'never' ensures it doesn't try to pop open a browser 
     automatically if you're running in a restricted terminal environment.
  */
  reporter: [
    ['list'], 
    ['html', { outputFolder: 'playwright-report', open: 'never' }]
  ],
  timeout: 30 * 1000,
  retries: 1,
  globalSetup: './tests/ui/global-setup.ts',
  expect: {
    timeout: 5000,
  },
  use: {
    baseURL: BASE_URL,
    headless: true,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 0,
    ignoreHTTPSErrors: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',      // Store Playwright trace logs
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
})