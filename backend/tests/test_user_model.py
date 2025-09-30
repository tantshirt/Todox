"""
User model validation tests
"""
import pytest
from pydantic import ValidationError
from datetime import datetime

from src.models.user import UserBase, UserCreate, UserInDB, UserResponse


def test_user_base_valid_email():
    """Test UserBase accepts valid email"""
    user = UserBase(email="test@example.com")
    assert user.email == "test@example.com"


def test_user_base_invalid_email():
    """Test UserBase rejects invalid email format"""
    with pytest.raises(ValidationError) as exc_info:
        UserBase(email="not-an-email")
    
    assert "value is not a valid email address" in str(exc_info.value)


def test_user_create_valid():
    """Test UserCreate with valid data"""
    user = UserCreate(email="test@example.com", password="password123")
    assert user.email == "test@example.com"
    assert user.password == "password123"


def test_user_create_short_password():
    """Test UserCreate rejects password < 8 characters"""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(email="test@example.com", password="short")
    
    assert "at least 8 characters" in str(exc_info.value).lower()


def test_user_in_db_all_fields():
    """Test UserInDB creation with all required fields"""
    now = datetime.utcnow()
    user = UserInDB(
        id="507f1f77bcf86cd799439011",
        email="test@example.com",
        hashed_password="$2b$12$hashed",
        created_at=now,
        updated_at=now
    )
    
    assert user.id == "507f1f77bcf86cd799439011"
    assert user.email == "test@example.com"
    assert user.hashed_password == "$2b$12$hashed"
    assert user.created_at == now
    assert user.updated_at == now


def test_user_response_excludes_password():
    """Test UserResponse doesn't have hashed_password field"""
    now = datetime.utcnow()
    user = UserResponse(
        id="507f1f77bcf86cd799439011",
        email="test@example.com",
        created_at=now,
        updated_at=now
    )
    
    assert user.id == "507f1f77bcf86cd799439011"
    assert user.email == "test@example.com"
    assert not hasattr(user, 'hashed_password')
