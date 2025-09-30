"""
Task API endpoint tests
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from bson import ObjectId

from src.repositories.user_repository import UserRepository
from src.core.security import hash_password, create_access_token


@pytest_asyncio.fixture
async def auth_user(test_db):
    """Create a test user for authentication"""
    user_repo = UserRepository(test_db)
    return await user_repo.create_user(
        email="taskuser@example.com",
        hashed_password=hash_password("password123")
    )


@pytest_asyncio.fixture
def auth_headers(auth_user):
    """Generate valid auth headers for testing"""
    token = create_access_token(auth_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_task_success(async_client: AsyncClient, auth_headers: dict):
    """Test successful task creation"""
    task_data = {
        "title": "Test Task",
        "description": "Test description",
        "priority": "High",
        "deadline": "2025-12-31",
        "label_ids": []
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test description"
    assert data["priority"] == "High"
    assert data["deadline"] == "2025-12-31"
    assert data["status"] == "open"
    assert data["label_ids"] == []
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_task_requires_authentication(async_client: AsyncClient):
    """Test POST /tasks without token returns 401"""
    task_data = {
        "title": "Test Task",
        "priority": "High",
        "deadline": "2025-12-31"
    }
    
    response = await async_client.post("/tasks", json=task_data)
    
    # HTTPBearer returns 403 for missing auth
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_task_missing_title(async_client: AsyncClient, auth_headers: dict):
    """Test POST without title returns 422 validation error"""
    task_data = {
        "priority": "High",
        "deadline": "2025-12-31"
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_invalid_priority(async_client: AsyncClient, auth_headers: dict):
    """Test POST with invalid priority returns 422"""
    task_data = {
        "title": "Test Task",
        "priority": "Invalid",
        "deadline": "2025-12-31"
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_invalid_deadline(async_client: AsyncClient, auth_headers: dict):
    """Test POST with invalid deadline format returns 422"""
    task_data = {
        "title": "Test Task",
        "priority": "High",
        "deadline": "not-a-date"
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_defaults(async_client: AsyncClient, auth_headers: dict):
    """Test task created with default status='open' and label_ids=[]"""
    task_data = {
        "title": "Test Task",
        "priority": "Medium",
        "deadline": "2025-12-31"
        # No label_ids provided
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "open"
    assert data["label_ids"] == []


@pytest.mark.asyncio
async def test_create_task_owner_id_from_token(async_client: AsyncClient, auth_headers: dict, auth_user):
    """Test created task has owner_id matching authenticated user"""
    task_data = {
        "title": "Test Task",
        "priority": "Low",
        "deadline": "2025-12-31"
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["owner_id"] == auth_user.id


# GET /tasks tests
@pytest.mark.asyncio
async def test_get_tasks_authenticated_user(async_client: AsyncClient, auth_headers: dict):
    """Test authenticated user can get their tasks"""
    # Create a task first
    await async_client.post(
        "/tasks",
        json={"title": "Task 1", "priority": "High", "deadline": "2025-12-31"},
        headers=auth_headers
    )
    
    # Get tasks
    response = await async_client.get("/tasks", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == "Task 1"


@pytest.mark.asyncio
async def test_get_tasks_empty_array(async_client: AsyncClient, test_db):
    """Test GET /tasks returns empty array for user with no tasks"""
    # Create a new user with no tasks
    user_repo = UserRepository(test_db)
    new_user = await user_repo.create_user(
        email="notasks@example.com",
        hashed_password=hash_password("password123")
    )
    
    token = create_access_token(new_user.id)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await async_client.get("/tasks", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_get_tasks_requires_authentication(async_client: AsyncClient):
    """Test GET /tasks without token returns 403"""
    response = await async_client.get("/tasks")
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_tasks_ownership_isolation(async_client: AsyncClient, test_db):
    """Test user A cannot see user B's tasks"""
    user_repo = UserRepository(test_db)
    
    # Create user A and their task
    user_a = await user_repo.create_user(
        email="usera@example.com",
        hashed_password=hash_password("password123")
    )
    token_a = create_access_token(user_a.id)
    headers_a = {"Authorization": f"Bearer {token_a}"}
    
    await async_client.post(
        "/tasks",
        json={"title": "User A Task", "priority": "High", "deadline": "2025-12-31"},
        headers=headers_a
    )
    
    # Create user B
    user_b = await user_repo.create_user(
        email="userb@example.com",
        hashed_password=hash_password("password123")
    )
    token_b = create_access_token(user_b.id)
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    # User B gets their tasks
    response = await async_client.get("/tasks", headers=headers_b)
    
    assert response.status_code == 200
    data = response.json()
    # User B should have no tasks (user A's task not visible)
    assert data == []


@pytest.mark.asyncio
async def test_get_tasks_sorted_newest_first(async_client: AsyncClient, auth_headers: dict):
    """Test tasks are sorted by created_at descending (newest first)"""
    # Create multiple tasks
    task1_response = await async_client.post(
        "/tasks",
        json={"title": "First Task", "priority": "High", "deadline": "2025-12-31"},
        headers=auth_headers
    )
    task1_id = task1_response.json()["id"]
    
    task2_response = await async_client.post(
        "/tasks",
        json={"title": "Second Task", "priority": "High", "deadline": "2025-12-31"},
        headers=auth_headers
    )
    task2_id = task2_response.json()["id"]
    
    # Get tasks
    response = await async_client.get("/tasks", headers=auth_headers)
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2
    
    # Find our tasks in the list
    our_tasks = [t for t in tasks if t["id"] in [task1_id, task2_id]]
    assert len(our_tasks) == 2
    
    # Newest (task2) should come before task1
    task2_index = next(i for i, t in enumerate(tasks) if t["id"] == task2_id)
    task1_index = next(i for i, t in enumerate(tasks) if t["id"] == task1_id)
    assert task2_index < task1_index


# PATCH /tasks/{id} tests
@pytest.mark.asyncio
async def test_update_task_partial_update(async_client: AsyncClient, auth_headers: dict):
    """Test updating only some fields of a task"""
    # Create a task
    create_response = await async_client.post(
        "/tasks",
        json={"title": "Original Title", "priority": "High", "deadline": "2025-12-31"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Update only title
    response = await async_client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated Title"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["priority"] == "High"  # Unchanged


@pytest.mark.asyncio
async def test_update_task_not_found(async_client: AsyncClient, auth_headers: dict):
    """Test updating non-existent task returns 404"""
    fake_id = str(ObjectId())
    
    response = await async_client.patch(
        f"/tasks/{fake_id}",
        json={"title": "Updated"},
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_ownership_check(async_client: AsyncClient, test_db):
    """Test user cannot update another user's task"""
    user_repo = UserRepository(test_db)
    
    # User A creates a task
    user_a = await user_repo.create_user(
        email="updatea@example.com",
        hashed_password=hash_password("password123")
    )
    token_a = create_access_token(user_a.id)
    headers_a = {"Authorization": f"Bearer {token_a}"}
    
    create_response = await async_client.post(
        "/tasks",
        json={"title": "User A Task", "priority": "High", "deadline": "2025-12-31"},
        headers=headers_a
    )
    task_id = create_response.json()["id"]
    
    # User B tries to update it
    user_b = await user_repo.create_user(
        email="updateb@example.com",
        hashed_password=hash_password("password123")
    )
    token_b = create_access_token(user_b.id)
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    response = await async_client.patch(
        f"/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=headers_b
    )
    
    assert response.status_code == 404  # Returns 404, not 403 (prevents enumeration)


# DELETE /tasks/{id} tests
@pytest.mark.asyncio
async def test_delete_task_success(async_client: AsyncClient, auth_headers: dict):
    """Test deleting a task returns 204"""
    # Create a task
    create_response = await async_client.post(
        "/tasks",
        json={"title": "To Delete", "priority": "Low", "deadline": "2025-12-31"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Delete it
    response = await async_client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_task_actually_removed(async_client: AsyncClient, auth_headers: dict):
    """Test deleted task cannot be retrieved"""
    # Create and delete a task
    create_response = await async_client.post(
        "/tasks",
        json={"title": "To Delete", "priority": "Low", "deadline": "2025-12-31"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    await async_client.delete(f"/tasks/{task_id}", headers=auth_headers)
    
    # Try to get tasks - should not include deleted task
    response = await async_client.get("/tasks", headers=auth_headers)
    task_ids = [t["id"] for t in response.json()]
    assert task_id not in task_ids


@pytest.mark.asyncio
async def test_delete_task_not_found(async_client: AsyncClient, auth_headers: dict):
    """Test deleting non-existent task returns 404"""
    fake_id = str(ObjectId())
    
    response = await async_client.delete(
        f"/tasks/{fake_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_ownership_check(async_client: AsyncClient, test_db):
    """Test user cannot delete another user's task"""
    user_repo = UserRepository(test_db)
    
    # User A creates a task
    user_a = await user_repo.create_user(
        email="deletea@example.com",
        hashed_password=hash_password("password123")
    )
    token_a = create_access_token(user_a.id)
    headers_a = {"Authorization": f"Bearer {token_a}"}
    
    create_response = await async_client.post(
        "/tasks",
        json={"title": "User A Task", "priority": "High", "deadline": "2025-12-31"},
        headers=headers_a
    )
    task_id = create_response.json()["id"]
    
    # User B tries to delete it
    user_b = await user_repo.create_user(
        email="deleteb@example.com",
        hashed_password=hash_password("password123")
    )
    token_b = create_access_token(user_b.id)
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    response = await async_client.delete(
        f"/tasks/{task_id}",
        headers=headers_b
    )
    
    assert response.status_code == 404
