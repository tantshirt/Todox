"""
Label API endpoint tests
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.repositories.user_repository import UserRepository
from src.core.security import hash_password, create_access_token


@pytest_asyncio.fixture
async def label_user(test_db):
    """Create a test user for label operations"""
    user_repo = UserRepository(test_db)
    return await user_repo.create_user(
        email="labeluser@example.com",
        hashed_password=hash_password("password123")
    )


@pytest_asyncio.fixture
def label_auth_headers(label_user):
    """Generate auth headers for label user"""
    token = create_access_token(label_user.id)
    return {"Authorization": f"Bearer {token}"}


# POST /labels tests
@pytest.mark.asyncio
async def test_create_label_success(async_client: AsyncClient, label_auth_headers: dict):
    """Test creating a label successfully"""
    response = await async_client.post(
        "/labels",
        json={"name": "Work"},
        headers=label_auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Work"
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_label_duplicate_name(async_client: AsyncClient, label_auth_headers: dict):
    """Test creating duplicate label name returns 409"""
    # Create first label
    await async_client.post(
        "/labels",
        json={"name": "Duplicate"},
        headers=label_auth_headers
    )
    
    # Try to create duplicate
    response = await async_client.post(
        "/labels",
        json={"name": "Duplicate"},
        headers=label_auth_headers
    )
    
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


# GET /labels tests
@pytest.mark.asyncio
async def test_get_labels_sorted_alphabetically(async_client: AsyncClient, label_auth_headers: dict):
    """Test GET /labels returns labels sorted alphabetically"""
    # Create labels in random order
    await async_client.post("/labels", json={"name": "Zebra"}, headers=label_auth_headers)
    await async_client.post("/labels", json={"name": "Apple"}, headers=label_auth_headers)
    await async_client.post("/labels", json={"name": "Mango"}, headers=label_auth_headers)
    
    response = await async_client.get("/labels", headers=label_auth_headers)
    
    assert response.status_code == 200
    labels = response.json()
    assert len(labels) >= 3
    
    # Find our labels
    our_labels = [l for l in labels if l["name"] in ["Zebra", "Apple", "Mango"]]
    assert our_labels[0]["name"] == "Apple"
    assert our_labels[1]["name"] == "Mango"
    assert our_labels[2]["name"] == "Zebra"


@pytest.mark.asyncio
async def test_get_labels_empty_array(async_client: AsyncClient, test_db):
    """Test GET /labels returns empty array for user with no labels"""
    user_repo = UserRepository(test_db)
    new_user = await user_repo.create_user(
        email="nolabels@example.com",
        hashed_password=hash_password("password123")
    )
    
    token = create_access_token(new_user.id)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await async_client.get("/labels", headers=headers)
    
    assert response.status_code == 200
    assert response.json() == []


# PATCH /labels/{id} tests
@pytest.mark.asyncio
async def test_update_label_success(async_client: AsyncClient, label_auth_headers: dict):
    """Test updating a label name"""
    # Create label
    create_response = await async_client.post(
        "/labels",
        json={"name": "OldName"},
        headers=label_auth_headers
    )
    label_id = create_response.json()["id"]
    
    # Update it
    response = await async_client.patch(
        f"/labels/{label_id}",
        json={"name": "NewName"},
        headers=label_auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "NewName"


@pytest.mark.asyncio
async def test_update_label_not_found(async_client: AsyncClient, label_auth_headers: dict):
    """Test updating non-existent label returns 404"""
    from bson import ObjectId
    
    response = await async_client.patch(
        f"/labels/{str(ObjectId())}",
        json={"name": "NewName"},
        headers=label_auth_headers
    )
    
    assert response.status_code == 404


# DELETE /labels/{id} tests
@pytest.mark.asyncio
async def test_delete_label_success(async_client: AsyncClient, label_auth_headers: dict):
    """Test deleting a label returns 204"""
    # Create label
    create_response = await async_client.post(
        "/labels",
        json={"name": "ToDelete"},
        headers=label_auth_headers
    )
    label_id = create_response.json()["id"]
    
    # Delete it
    response = await async_client.delete(
        f"/labels/{label_id}",
        headers=label_auth_headers
    )
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_label_cascade_from_tasks(async_client: AsyncClient, label_auth_headers: dict):
    """Test deleting label removes it from tasks"""
    # Create label
    label_response = await async_client.post(
        "/labels",
        json={"name": "CascadeTest"},
        headers=label_auth_headers
    )
    label_id = label_response.json()["id"]
    
    # Create task with this label
    task_response = await async_client.post(
        "/tasks",
        json={
            "title": "Task with label",
            "priority": "High",
            "deadline": "2025-12-31",
            "label_ids": [label_id]
        },
        headers=label_auth_headers
    )
    task_id = task_response.json()["id"]
    
    # Verify task has the label
    tasks_response = await async_client.get("/tasks", headers=label_auth_headers)
    task = next(t for t in tasks_response.json() if t["id"] == task_id)
    assert label_id in task["label_ids"]
    
    # Delete the label
    await async_client.delete(f"/labels/{label_id}", headers=label_auth_headers)
    
    # Verify label removed from task
    tasks_response = await async_client.get("/tasks", headers=label_auth_headers)
    task = next(t for t in tasks_response.json() if t["id"] == task_id)
    assert label_id not in task["label_ids"]
