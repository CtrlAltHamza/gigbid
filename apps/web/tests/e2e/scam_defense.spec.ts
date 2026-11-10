import { test, expect } from '@playwright/test';

test.describe('Scam Defense Guardrails', () => {
  test('flags scam job, displays red flags and reasoning, blocks draft generation', async ({ page }) => {
    await page.goto('/');

    // 1. Locate the crypto telegram scam job
    const scamCard = page.locator('text=URGENT: Crypto Trading Telegram Bot');
    await expect(scamCard).toBeVisible();

    // 2. Verify scam badge & blocked tag
    await expect(page.getByText('SCAM DETECTED')).toBeVisible();
    await expect(page.getByText('BLOCKED — Off-Platform Fraud')).toBeVisible();

    // 3. Verify scam guardrail explanation box is visible
    await expect(page.getByText('Scam Guardrail Triggered:')).toBeVisible();
    await expect(page.getByText('Demands off-platform communication via WhatsApp')).toBeVisible();

    // 4. Verify draft button is disabled
    const blockedBtn = page.getByRole('button', { name: 'Draft Blocked' });
    await expect(blockedBtn).toBeVisible();
    await expect(blockedBtn).toBeDisabled();
  });
});

