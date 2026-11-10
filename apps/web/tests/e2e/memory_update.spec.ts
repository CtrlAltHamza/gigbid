import { test, expect } from '@playwright/test';

test.describe('Memory Store & Self-Correction', () => {
  test('rejects proposal with feedback, verifies promotion to Memory Store, inspects rule in Settings', async ({ page }) => {
    await page.goto('/');

    // 1. Go to proposal studio
    await page.getByRole('button', { name: 'Review Draft' }).first().click();

    // 2. Click Reject & Teach
    const rejectBtn = page.getByRole('button', { name: 'Reject & Teach' });
    await expect(rejectBtn).toBeVisible();
    await rejectBtn.click();

    // 3. Modal appears
    await expect(page.getByText('Reject & Promote to Long-Term Memory')).toBeVisible();

    // 4. Fill feedback rule
    const textarea = page.locator('textarea').last();
    await textarea.fill('Never quote hourly rates under $75/hr and avoid promising unpaid exploratory sprints.');

    // 5. Submit rejection
    await page.getByRole('button', { name: 'Promote Rule & Reject' }).click();

    // 6. Navigate to Settings & Memory view
    await page.getByRole('button', { name: 'Settings & Memory' }).click();

    // 7. Verify new rule is present in the Memory Store list
    await expect(page.getByText('Never quote hourly rates under $75/hr and avoid promising unpaid exploratory sprints.')).toBeVisible();
  });
});

