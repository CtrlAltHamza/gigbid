import { test, expect } from '@playwright/test';

test.describe('Happy Path: Scouting to Submission', () => {
  test('scouts jobs, opens proposal studio, edits and approves, and verifies Connects deduction', async ({ page }) => {
    // 1. Visit the app
    await page.goto('/');

    // 2. Check inbox shows ranked jobs
    await expect(page.getByText('Marketplace Job Inbox')).toBeVisible();
    await expect(page.getByText('Production RAG Pipeline with Hybrid Search')).toBeVisible();

    // 3. Connects balance initially 150
    await expect(page.locator('text=150')).toBeVisible();

    // 4. Click Review Draft on top job
    await page.getByRole('button', { name: 'Review Draft' }).first().click();

    // 5. Land in Proposal Studio
    await expect(page.getByText('Proposal Content (Editable)')).toBeVisible();
    await expect(page.getByText('Critic Agent Rubric')).toBeVisible();

    // 6. Test Evidence Citation hover
    const citationBtn = page.getByRole('button', { name: '[CS-AI-01]' });
    await expect(citationBtn).toBeVisible();
    await citationBtn.hover();
    await expect(page.getByText('Sub-100ms Multimodal Hybrid RAG for FinTech Compliance')).toBeVisible();

    // 7. Click Approve & Submit
    const approveBtn = page.getByRole('button', { name: 'Approve & Submit' });
    await expect(approveBtn).toBeVisible();
    await approveBtn.click();

    // 8. Verify Connects deducted from 150 to 134
    await expect(page.locator('text=134')).toBeVisible();

    // 9. Status badge changes to Submitted
    await expect(page.locator('text=Submitted')).toBeVisible();
  });
});

