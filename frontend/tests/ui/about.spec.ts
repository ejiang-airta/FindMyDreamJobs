// File: frontend/tests/ui/about.spec.ts
import { test, expect } from '@playwright/test'
import { BASE_URL } from './test-config'

test.describe('About', () => {

  test('Test# 32: About page renders mission and value', async ({ page }) => {
    await page.goto(`${BASE_URL}/about`, { waitUntil: 'domcontentloaded', timeout: 60000 })

    await expect(page.getByRole('heading', { name: /Our Mission/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Our Values/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Innovation/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Transparency/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: /User-First/ })).toBeVisible()
  })

})
