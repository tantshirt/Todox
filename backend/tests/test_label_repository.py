"""
Label repository tests
"""
import pytest
import pytest_asyncio
from bson import ObjectId
from fastapi import HTTPException

from src.repositories.label_repository import LabelRepository
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository
from src.core.security import hash_password
from datetime import date


@pytest_asyncio.fixture
async def test_user(test_db):
    """Create a test user for label ownership"""
    user_repo = UserRepository(test_db)
    return await user_repo.create_user(
        email="labelowner@example.com",
        hashed_password=hash_password("password123")
    )


@pytest.mark.asyncio
async def test_create_label_success(test_db, test_user):
    """Test creating a label successfully"""
    repo = LabelRepository(test_db)
    
    label = await repo.create_label("Work", ObjectId(test_user.id))
    
    assert label.id is not None
    assert label.name == "Work"
    assert label.owner_id == test_user.id
    assert label.created_at is not None


@pytest.mark.asyncio
async def test_create_label_duplicate_name_same_user(test_db, test_user):
    """Test creating duplicate label name for same user raises 409"""
    repo = LabelRepository(test_db)
    await repo.ensure_indexes()
    
    # Create first label
    await repo.create_label("Work", ObjectId(test_user.id))
    
    # Try to create duplicate
    with pytest.raises(HTTPException) as exc_info:
        await repo.create_label("Work", ObjectId(test_user.id))
    
    assert exc_info.value.status_code == 409
    assert "already exists" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_label_same_name_different_users(test_db):
    """Test different users can have labels with same name"""
    user_repo = UserRepository(test_db)
    label_repo = LabelRepository(test_db)
    await label_repo.ensure_indexes()
    
    # Create two users
    user1 = await user_repo.create_user(
        email="user1@example.com",
        hashed_password=hash_password("password123")
    )
    user2 = await user_repo.create_user(
        email="user2@example.com",
        hashed_password=hash_password("password123")
    )
    
    # Both can create "Work" label
    label1 = await label_repo.create_label("Work", ObjectId(user1.id))
    label2 = await label_repo.create_label("Work", ObjectId(user2.id))
    
    assert label1.name == "Work"
    assert label2.name == "Work"
    assert label1.owner_id != label2.owner_id


@pytest.mark.asyncio
async def test_find_by_owner_sorted_alphabetically(test_db, test_user):
    """Test find_by_owner returns labels sorted by name"""
    repo = LabelRepository(test_db)
    
    # Create labels in random order
    await repo.create_label("Zebra", ObjectId(test_user.id))
    await repo.create_label("Apple", ObjectId(test_user.id))
    await repo.create_label("Mango", ObjectId(test_user.id))
    
    labels = await repo.find_by_owner(ObjectId(test_user.id))
    
    assert len(labels) == 3
    assert labels[0].name == "Apple"
    assert labels[1].name == "Mango"
    assert labels[2].name == "Zebra"


@pytest.mark.asyncio
async def test_find_by_id_with_ownership(test_db, test_user):
    """Test find_by_id returns label if owner matches"""
    repo = LabelRepository(test_db)
    
    created_label = await repo.create_label("Personal", ObjectId(test_user.id))
    
    found_label = await repo.find_by_id(ObjectId(created_label.id), ObjectId(test_user.id))
    
    assert found_label is not None
    assert found_label.id == created_label.id
    assert found_label.name == "Personal"


@pytest.mark.asyncio
async def test_find_by_id_ownership_check(test_db, test_user):
    """Test find_by_id returns None if owner doesn't match"""
    repo = LabelRepository(test_db)
    
    created_label = await repo.create_label("Personal", ObjectId(test_user.id))
    
    # Try to find with different owner_id
    found_label = await repo.find_by_id(ObjectId(created_label.id), ObjectId())
    
    assert found_label is None


@pytest.mark.asyncio
async def test_update_label_success(test_db, test_user):
    """Test updating a label name"""
    repo = LabelRepository(test_db)
    
    created_label = await repo.create_label("OldName", ObjectId(test_user.id))
    
    updated_label = await repo.update_label(
        ObjectId(created_label.id),
        ObjectId(test_user.id),
        "NewName"
    )
    
    assert updated_label is not None
    assert updated_label.name == "NewName"
    assert updated_label.id == created_label.id


@pytest.mark.asyncio
async def test_update_label_duplicate_name(test_db, test_user):
    """Test updating to duplicate name raises 409"""
    repo = LabelRepository(test_db)
    await repo.ensure_indexes()
    
    # Create two labels
    label1 = await repo.create_label("Label1", ObjectId(test_user.id))
    await repo.create_label("Label2", ObjectId(test_user.id))
    
    # Try to rename label1 to "Label2"
    with pytest.raises(HTTPException) as exc_info:
        await repo.update_label(ObjectId(label1.id), ObjectId(test_user.id), "Label2")
    
    assert exc_info.value.status_code == 409


@pytest.mark.asyncio
async def test_delete_label_success(test_db, test_user):
    """Test deleting a label"""
    repo = LabelRepository(test_db)
    
    created_label = await repo.create_label("ToDelete", ObjectId(test_user.id))
    
    result = await repo.delete_label(ObjectId(created_label.id), ObjectId(test_user.id))
    
    assert result is True
    
    # Verify it's gone
    found = await repo.find_by_id(ObjectId(created_label.id), ObjectId(test_user.id))
    assert found is None


@pytest.mark.asyncio
async def test_delete_label_cascade_from_tasks(test_db, test_user):
    """Test deleting label removes it from tasks' label_ids"""
    label_repo = LabelRepository(test_db)
    task_repo = TaskRepository(test_db)
    
    # Create a label
    label = await label_repo.create_label("Urgent", ObjectId(test_user.id))
    
    # Create a task with this label
    task = await task_repo.create_task({
        "title": "Test Task",
        "priority": "High",
        "deadline": date(2025, 12, 31),
        "owner_id": ObjectId(test_user.id),
        "label_ids": [label.id]
    })
    
    assert task.label_ids == [label.id]
    
    # Delete the label
    await label_repo.delete_label(ObjectId(label.id), ObjectId(test_user.id))
    
    # Verify task's label_ids no longer includes deleted label
    updated_task = await task_repo.find_by_id(ObjectId(task.id), ObjectId(test_user.id))
    assert updated_task is not None
    assert label.id not in updated_task.label_ids
    assert updated_task.label_ids == []


@pytest.mark.asyncio
async def test_delete_label_not_found(test_db, test_user):
    """Test deleting non-existent label returns False"""
    repo = LabelRepository(test_db)
    
    result = await repo.delete_label(ObjectId(), ObjectId(test_user.id))
    
    assert result is False
