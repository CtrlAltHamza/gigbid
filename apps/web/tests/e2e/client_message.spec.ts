import { test, expect } from '@playwright/test';

test.describe('Client Messaging & Workspace MCP', () => {
  test('receives client message, classifies interview intent, books calendar hold via Workspace MCP', async ({ page }) => {
    await page.goto('/');

    // 1. Navigate to Client Messages tab
    await page.getByRole('button', { name: 'Client Messages' }).click();

    // 2. Verify active conversation and intent badge
    await expect(page.getByText('Dr. Eleanor Vance (HealthTech)')).toBeVisible();
    await expect(page.getByText('Interview Invite')).toBeVisible();

    // 3. Verify Workspace MCP calendar widget is visible
    await expect(page.getByText('Workspace MCP: Calendar Hold Availability')).toBeVisible();

    // 4. Click first available slot
    const slotBtn = page.getByRole('button', { name: /Slot 1/ }).first();
    await expect(slotBtn).toBeVisible();
    await slotBtn.click();

    // 5. Verify hold confirmed
    await expect(page.getByText('Hold Confirmed')).toBeVisible();
    await expect(page.getByText('Interview hold confirmed via Workspace MCP')).toBeVisible();
  });
});

