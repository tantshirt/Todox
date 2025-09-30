"""
Task model validation tests
"""
import pytest
from pydantic import ValidationError
from datetime import date, datetime

from src.models.task import TaskBase, TaskCreate, TaskUpdate, TaskInDB


def test_task_base_valid_data():
    """Test TaskBase accepts valid task data"""
    task = TaskBase(
        title="Test Task",
        description="Test description",
        priority="High",
        deadline=date(2025, 12, 31)
    )
    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.priority == "High"
    assert task.deadline == date(2025, 12, 31)


def test_task_title_empty_rejected():
    """Test TaskBase rejects empty title"""
    with pytest.raises(ValidationError) as exc_info:
        TaskBase(
            title="",
            priority="High",
            deadline=date(2025, 12, 31)
        )
    
    assert "at least 1 character" in str(exc_info.value).lower()


def test_task_title_too_long_rejected():
    """Test TaskBase rejects title > 200 characters"""
    long_title = "a" * 201
    
    with pytest.raises(ValidationError) as exc_info:
        TaskBase(
            title=long_title,
            priority="High",
            deadline=date(2025, 12, 31)
        )
    
    assert "at most 200 characters" in str(exc_info.value).lower()


def test_task_invalid_priority_rejected():
    """Test TaskBase rejects invalid priority value"""
    with pytest.raises(ValidationError):
        TaskBase(
            title="Test",
            priority="Invalid",  # Not in Literal['High', 'Medium', 'Low']
            deadline=date(2025, 12, 31)
        )


def test_task_invalid_deadline_rejected():
    """Test TaskBase rejects invalid date format"""
    with pytest.raises(ValidationError):
        TaskBase(
            title="Test",
            priority="High",
            deadline="not-a-date"  # Should be date object
        )


def test_task_description_optional():
    """Test description field is optional"""
    task = TaskBase(
        title="Test",
        priority="Medium",
        deadline=date(2025, 12, 31)
    )
    assert task.description is None


def test_task_create_defaults():
    """Test TaskCreate default values"""
    task = TaskCreate(
        title="Test",
        priority="Low",
        deadline=date(2025, 12, 31)
    )
    assert task.label_ids == []


def test_task_in_db_all_fields():
    """Test TaskInDB with all required fields"""
    now = datetime.utcnow()
    task = TaskInDB(
        id="507f1f77bcf86cd799439011",
        title="Test Task",
        description="Description",
        priority="High",
        deadline=date(2025, 12, 31),
        status="open",
        label_ids=["label1", "label2"],
        owner_id="507f191e810c19729de860ea",
        created_at=now,
        updated_at=now
    )
    
    assert task.id == "507f1f77bcf86cd799439011"
    assert task.title == "Test Task"
    assert task.status == "open"
    assert task.label_ids == ["label1", "label2"]
    assert task.owner_id == "507f191e810c19729de860ea"


def test_task_update_all_optional():
    """Test TaskUpdate accepts partial data"""
    # Update only title
    task_update = TaskUpdate(title="New Title")
    assert task_update.title == "New Title"
    assert task_update.priority is None
    
    # Update only status
    task_update2 = TaskUpdate(status="done")
    assert task_update2.status == "done"
    assert task_update2.title is None
