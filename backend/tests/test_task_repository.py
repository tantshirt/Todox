"""
Task repository tests
"""
import pytest
import pytest_asyncio
from bson import ObjectId
from datetime import date

from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.core.security import hash_password


@pytest_asyncio.fixture
async def test_user(test_db):
    """Create a test user for task ownership"""
    user_repo = UserRepository(test_db)
    return await user_repo.create_user(
        email="taskowner@example.com",
        hashed_password=hash_password("password123")
    )


@pytest_asyncio.fixture
async def test_task(test_db, test_user):
    """Create a test task"""
    task_repo = TaskRepository(test_db)
    task_data = {
        "title": "Test Task",
        "description": "Test description",
        "priority": "High",
        "deadline": date(2025, 12, 31),
        "owner_id": ObjectId(test_user.id)
    }
    return await task_repo.create_task(task_data)


@pytest.mark.asyncio
async def test_create_task_success(test_db, test_user):
    """Test create_task inserts document and returns TaskInDB with id"""
    repo = TaskRepository(test_db)
    
    task_data = {
        "title": "New Task",
        "priority": "Medium",
        "deadline": date(2025, 12, 31),
        "owner_id": ObjectId(test_user.id)
    }
    
    task = await repo.create_task(task_data)
    
    assert task.id is not None
    assert task.title == "New Task"
    assert task.priority == "Medium"
    assert task.status == "open"  # Default
    assert task.label_ids == []  # Default
    assert task.owner_id == test_user.id
    assert task.created_at is not None
    assert task.updated_at is not None


@pytest.mark.asyncio
async def test_find_by_owner_returns_user_tasks(test_db, test_user, test_task):
    """Test find_by_owner returns only tasks for specified owner_id"""
    repo = TaskRepository(test_db)
    
    # Create another task for the same user
    await repo.create_task({
        "title": "Task 2",
        "priority": "Low",
        "deadline": date(2025, 11, 30),
        "owner_id": ObjectId(test_user.id)
    })
    
    tasks = await repo.find_by_owner(ObjectId(test_user.id))
    
    assert len(tasks) == 2
    assert all(task.owner_id == test_user.id for task in tasks)


@pytest.mark.asyncio
async def test_find_by_owner_empty_list(test_db):
    """Test find_by_owner returns empty list if no tasks"""
    repo = TaskRepository(test_db)
    
    tasks = await repo.find_by_owner(ObjectId())
    
    assert tasks == []


@pytest.mark.asyncio
async def test_find_by_owner_sorted_descending(test_db, test_user):
    """Test find_by_owner returns tasks sorted by created_at descending"""
    repo = TaskRepository(test_db)
    
    # Create tasks in order
    task1 = await repo.create_task({
        "title": "First Task",
        "priority": "High",
        "deadline": date(2025, 12, 31),
        "owner_id": ObjectId(test_user.id)
    })
    
    task2 = await repo.create_task({
        "title": "Second Task",
        "priority": "High",
        "deadline": date(2025, 12, 31),
        "owner_id": ObjectId(test_user.id)
    })
    
    tasks = await repo.find_by_owner(ObjectId(test_user.id))
    
    # Newest (task2) should be first
    assert tasks[0].id == task2.id
    assert tasks[1].id == task1.id


@pytest.mark.asyncio
async def test_find_by_id_returns_task_if_owner_matches(test_db, test_user, test_task):
    """Test find_by_id returns task if owner matches"""
    repo = TaskRepository(test_db)
    
    found_task = await repo.find_by_id(ObjectId(test_task.id), ObjectId(test_user.id))
    
    assert found_task is not None
    assert found_task.id == test_task.id
    assert found_task.title == test_task.title


@pytest.mark.asyncio
async def test_find_by_id_returns_none_if_owner_mismatch(test_db, test_task):
    """Test find_by_id returns None if owner doesn't match (ownership check)"""
    repo = TaskRepository(test_db)
    
    # Try to access with different owner_id
    different_owner = ObjectId()
    found_task = await repo.find_by_id(ObjectId(test_task.id), different_owner)
    
    assert found_task is None


@pytest.mark.asyncio
async def test_update_task_updates_fields(test_db, test_user, test_task):
    """Test update_task updates specified fields and sets updated_at"""
    repo = TaskRepository(test_db)
    
    original_updated_at = test_task.updated_at
    
    # Update title and priority
    update_data = {
        "title": "Updated Title",
        "priority": "Low"
    }
    
    updated_task = await repo.update_task(
        ObjectId(test_task.id),
        ObjectId(test_user.id),
        update_data
    )
    
    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.priority == "Low"
    assert updated_task.description == test_task.description  # Unchanged
    assert updated_task.updated_at > original_updated_at


@pytest.mark.asyncio
async def test_delete_task_removes_task(test_db, test_user, test_task):
    """Test delete_task removes task and returns True"""
    repo = TaskRepository(test_db)
    
    result = await repo.delete_task(ObjectId(test_task.id), ObjectId(test_user.id))
    
    assert result is True
    
    # Verify task is gone
    found = await repo.find_by_id(ObjectId(test_task.id), ObjectId(test_user.id))
    assert found is None


@pytest.mark.asyncio
async def test_delete_task_returns_false_if_not_found(test_db, test_user):
    """Test delete_task returns False if task not found"""
    repo = TaskRepository(test_db)
    
    result = await repo.delete_task(ObjectId(), ObjectId(test_user.id))
    
    assert result is False


@pytest.mark.asyncio
async def test_delete_task_returns_false_if_owner_mismatch(test_db, test_task):
    """Test delete_task returns False if owner doesn't match"""
    repo = TaskRepository(test_db)
    
    # Try to delete with wrong owner
    result = await repo.delete_task(ObjectId(test_task.id), ObjectId())
    
    assert result is False
    
    # Task should still exist
    found = await repo.find_by_id(ObjectId(test_task.id), ObjectId(test_task.owner_id))
    assert found is not None
