import { test, expect } from '@playwright/test';

test.describe('Degraded Mode & Simulator Fallback', () => {
  test('simulates marketplace outage, verifies degraded mode banner, verifies drafts continue seamlessly', async ({ page }) => {
    await page.goto('/');

    // 1. Initially live adapter connected
    await expect(page.getByText('Upwork Live Adapter Connected')).toBeVisible();

    // 2. Click Simulate Failure
    await page.getByRole('button', { name: 'Simulate Failure' }).click();

    // 3. Degraded mode banner appears
    await expect(page.getByText('Degraded Mode Active: GigSim Simulator Fallback')).toBeVisible();

    // 4. Verify user can still inspect and review drafts without interruption
    await page.getByRole('button', { name: 'Review Draft' }).first().click();
    await expect(page.getByText('Proposal Content (Editable)')).toBeVisible();

    // 5. Restore live adapter
    await page.getByRole('button', { name: 'Restore Live' }).click();
    await expect(page.getByText('Upwork Live Adapter Connected')).toBeVisible();
  });
});
