import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('complete auth flow: register → login → access protected route', async ({ page }) => {
    const timestamp = Date.now();
    const testEmail = `test-${timestamp}@example.com`;
    const testPassword = 'testpassword123';

    // Step 1: Registration
    await page.goto('/auth/register');
    
    await page.fill('input[type="email"]', testEmail);
    await page.fill('input[type="password"]', testPassword);
    await page.click('button[type="submit"]');
    
    // Should redirect to login page
    await page.waitForURL('/auth/login', { timeout: 5000 });
    
    // Should see success toast
    await expect(page.locator('text=/registration successful/i')).toBeVisible({ timeout: 3000 });
    
    // Step 2: Login with registered credentials
    await page.fill('input[type="email"]', testEmail);
    await page.fill('input[type="password"]', testPassword);
    await page.click('button[type="submit"]');
    
    // Should redirect to tasks page
    await page.waitForURL('/tasks', { timeout: 5000 });
    
    // Should see tasks page content
    await expect(page.locator('h1:has-text("Tasks")')).toBeVisible();
    
    // Should see welcome message with email
    await expect(page.locator(`text=/Welcome.*${testEmail}/i`)).toBeVisible();
    
    // Step 3: Verify token is stored
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeTruthy();
    expect(token).toMatch(/^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/); // JWT format
    
    // Step 4: Test logout
    await page.click('button:has-text("Logout")');
    
    // Should redirect to login
    await page.waitForURL('/auth/login', { timeout: 5000 });
    
    // Token should be cleared
    const tokenAfterLogout = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(tokenAfterLogout).toBeNull();
  });

  test('protected route redirects to login when not authenticated', async ({ page }) => {
    // Clear any existing auth
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    
    // Try to access protected route
    await page.goto('/tasks');
    
    // Should redirect to login
    await page.waitForURL('/auth/login', { timeout: 5000 });
  });

  test('validation errors display correctly', async ({ page }) => {
    await page.goto('/auth/register');
    
    // Test invalid email
    await page.fill('input[type="email"]', 'not-an-email');
    await page.fill('input[type="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // Should show email validation error
    await expect(page.locator('text=/invalid email/i')).toBeVisible();
    
    // Test short password
    await page.fill('input[type="email"]', 'test@example.com');
    await page.fill('input[type="password"]', 'short');
    await page.click('button[type="submit"]');
    
    // Should show password validation error
    await expect(page.locator('text=/at least 8 characters/i')).toBeVisible();
  });
});
