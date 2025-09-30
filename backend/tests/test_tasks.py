"""
Task API endpoint tests
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

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
