// ✅ File: frontend/playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/ui',
  timeout: 30 * 1000,
  retries: 1,
  globalSetup: './tests/ui/global-setup.ts',
  expect: {
    timeout: 5000,
  },
  use: {
    // Use the variable from GitLab to point to preview env, or fallback to production
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'https://findmydreamjobs.com',
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
