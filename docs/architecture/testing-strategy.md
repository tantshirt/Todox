# Testing Strategy

## Testing Pyramid

```
        E2E Tests (Playwright)
       /                      \
      /   Integration Tests     \
     /    (Backend API tests)     \
    /                              \
   /     Frontend Unit Tests        \
  /    (Vitest) Backend Unit Tests   \
 /              (Pytest)              \
------------------------------------------------
```

## Test Organization

### Frontend Tests

```
frontend/src/
├── components/
│   └── tasks/
│       ├── TaskCard.tsx
│       └── TaskCard.test.tsx        # Component unit tests
├── lib/
│   └── utils.test.ts                 # Utility function tests
└── hooks/
    └── useTasks.test.ts              # Hook tests (minimal, mostly covered by E2E)
```

### Backend Tests

```
backend/tests/
├── conftest.py                       # Pytest fixtures (test DB, test client)
├── test_auth.py                      # Auth endpoint integration tests
├── test_tasks.py                     # Task endpoint integration tests
├── test_labels.py                    # Label endpoint integration tests
├── test_repositories.py              # Repository unit tests
└── test_services.py                  # Service layer unit tests
```

### E2E Tests

```
e2e/tests/
├── auth.spec.ts                      # Registration, login, logout flows
├── tasks.spec.ts                     # Task CRUD operations
└── labels.spec.ts                    # Label management and assignment
```

## Test Examples

### Frontend Component Test

```typescript
// components/tasks/TaskCard.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';
import { Task } from '@/types/models';

describe('TaskCard', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'Test description',
    priority: 'High',
    deadline: '2025-01-15',
    status: 'open',
    label_ids: [],
    owner_id: 'user1',
    created_at: '2025-01-12T10:00:00Z',
    updated_at: '2025-01-12T10:00:00Z',
  };

  it('renders task details correctly', () => {
    render(
      <TaskCard
        task={mockTask}
        onEdit={jest.fn()}
        onDelete={jest.fn()}
        onToggleStatus={jest.fn()}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('High')).toBeInTheDocument();
    expect(screen.getByText(/Due:/)).toBeInTheDocument();
  });

  it('calls onToggleStatus when checkbox is clicked', () => {
    const mockToggle = jest.fn();
    render(
      <TaskCard
        task={mockTask}
        onEdit={jest.fn()}
        onDelete={jest.fn()}
        onToggleStatus={mockToggle}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    expect(mockToggle).toHaveBeenCalledWith('1', 'done');
  });
});
```

### Backend API Test

```python
# tests/test_tasks.py

import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient, auth_headers: dict):
    """Test creating a new task."""
    task_data = {
        "title": "Test Task",
        "priority": "High",
        "deadline": "2025-01-15",
        "description": "Test description"
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "High"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_tasks_requires_auth(async_client: AsyncClient):
    """Test that getting tasks requires authentication."""
    response = await async_client.get("/tasks")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_task_not_owned(async_client: AsyncClient, auth_headers: dict, other_user_task_id: str):
    """Test that users cannot update tasks they don't own."""
    response = await async_client.patch(
        f"/tasks/{other_user_task_id}",
        json={"title": "Hacked"},
        headers=auth_headers
    )
    
    assert response.status_code == 404
```

### E2E Test

```typescript
// e2e/tests/tasks.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Register and login before each test
    await page.goto('/auth/register');
    await page.fill('input[type="email"]', `test-${Date.now()}@example.com`);
    await page.fill('input[type="password"]', 'testpassword123');
    await page.click('button[type="submit"]');
    
    await page.waitForURL('/auth/login');
    await page.fill('input[type="email"]', `test-${Date.now()}@example.com`);
    await page.fill('input[type="password"]', 'testpassword123');
    await page.click('button[type="submit"]');
    
    await page.waitForURL('/tasks');
  });

  test('create a new task', async ({ page }) => {
    // Click Create Task button
    await page.click('text=Create Task');
    
    // Fill in task details
    await page.fill('input[name="title"]', 'Buy groceries');
    await page.selectOption('select[name="priority"]', 'High');
    await page.fill('input[type="date"]', '2025-01-20');
    await page.fill('textarea[name="description"]', 'Milk, eggs, bread');
    
    // Submit form
    await page.click('button:has-text("Create Task")');
    
    // Verify task appears in list
    await expect(page.locator('text=Buy groceries')).toBeVisible();
    await expect(page.locator('text=High')).toBeVisible();
  });

  test('mark task as done', async ({ page }) => {
    // Create a task first
    await page.click('text=Create Task');
    await page.fill('input[name="title"]', 'Test Task');
    await page.selectOption('select[name="priority"]', 'Low');
    await page.fill('input[type="date"]', '2025-01-20');
    await page.click('button:has-text("Create Task")');
    
    // Check the task checkbox
    await page.check('input[type="checkbox"]');
    
    // Verify task title has strikethrough
    const taskTitle = page.locator('h3:has-text("Test Task")');
    await expect(taskTitle).toHaveClass(/line-through/);
  });
});
```

---
