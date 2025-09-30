"""
User repository tests
"""
import pytest
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user_success(test_db):
    """Test create_user inserts document and returns UserInDB"""
    repo = UserRepository(test_db)
    
    user = await repo.create_user(
        email="test@example.com",
        hashed_password="$2b$12$hashed"
    )
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.hashed_password == "$2b$12$hashed"
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_find_by_email_existing_user(test_db):
    """Test find_by_email finds existing user"""
    repo = UserRepository(test_db)
    
    # Create user first
    created_user = await repo.create_user(
        email="existing@example.com",
        hashed_password="$2b$12$hashed"
    )
    
    # Find by email
    found_user = await repo.find_by_email("existing@example.com")
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == "existing@example.com"


@pytest.mark.asyncio
async def test_find_by_email_non_existent(test_db):
    """Test find_by_email returns None for non-existent email"""
    repo = UserRepository(test_db)
    
    user = await repo.find_by_email("nonexistent@example.com")
    
    assert user is None


@pytest.mark.asyncio
async def test_find_by_id_success(test_db):
    """Test find_by_id finds user by ObjectId"""
    repo = UserRepository(test_db)
    
    # Create user
    created_user = await repo.create_user(
        email="findme@example.com",
        hashed_password="$2b$12$hashed"
    )
    
    # Find by ID
    found_user = await repo.find_by_id(ObjectId(created_user.id))
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == "findme@example.com"


@pytest.mark.asyncio
async def test_find_by_id_non_existent(test_db):
    """Test find_by_id returns None for non-existent ID"""
    repo = UserRepository(test_db)
    
    user = await repo.find_by_id(ObjectId())
    
    assert user is None


@pytest.mark.asyncio
async def test_email_uniqueness(test_db):
    """Test email uniqueness constraint prevents duplicate emails"""
    repo = UserRepository(test_db)
    
    # Ensure indexes are created
    await repo.ensure_indexes()
    
    # Create first user
    await repo.create_user(
        email="duplicate@example.com",
        hashed_password="$2b$12$hashed1"
    )
    
    # Attempt to create duplicate
    with pytest.raises(DuplicateKeyError):
        await repo.create_user(
            email="duplicate@example.com",
            hashed_password="$2b$12$hashed2"
        )
