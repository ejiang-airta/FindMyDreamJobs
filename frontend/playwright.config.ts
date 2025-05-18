// ✅ File: frontend/playwright.config.ts
import { defineConfig, devices } from '@playwright/test'
import path from 'path'

export default defineConfig({
  testDir: './tests/ui',
  timeout: 30 * 1000,
  retries: 1,
  outputDir: path.resolve(__dirname, 'test-results'), // <-- writes to frontend/test-results
  expect: {
    timeout: 5000,
  },
  use: {
    baseURL: 'https://findmydreamjobs.com',
    headless: true,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 0,
    ignoreHTTPSErrors: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
})
