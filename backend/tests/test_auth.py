"""
Authentication endpoint tests
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient, test_db):
    """Test successful user registration"""
    response = await async_client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "password123"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "hashed_password" not in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient, test_db):
    """Test registration with duplicate email returns 409"""
    email = "duplicate@example.com"
    
    # Register first user
    await async_client.post(
        "/auth/register",
        json={"email": email, "password": "password123"}
    )
    
    # Try to register again with same email
    response = await async_client.post(
        "/auth/register",
        json={"email": email, "password": "different456"}
    )
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_register_invalid_email(async_client: AsyncClient):
    """Test registration with invalid email format returns 422"""
    response = await async_client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": "password123"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_weak_password(async_client: AsyncClient):
    """Test registration with password < 8 characters returns 422"""
    response = await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "short"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_password_is_hashed(async_client: AsyncClient, test_db):
    """Test that password is hashed before storage"""
    plain_password = "password123"
    
    response = await async_client.post(
        "/auth/register",
        json={"email": "hashtest@example.com", "password": plain_password}
    )
    
    assert response.status_code == 201
    
    # Verify password was hashed in database
    from src.repositories.user_repository import UserRepository
    user_repo = UserRepository(test_db)
    user = await user_repo.find_by_email("hashtest@example.com")
    
    assert user is not None
    assert user.hashed_password != plain_password
    assert user.hashed_password.startswith("$2b$")  # Bcrypt hash prefix


@pytest.mark.asyncio
async def test_password_never_returned(async_client: AsyncClient):
    """Test that UserResponse excludes hashed_password field"""
    response = await async_client.post(
        "/auth/register",
        json={"email": "secure@example.com", "password": "password123"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Verify password fields are not in response
    assert "password" not in data
    assert "hashed_password" not in data
    assert "email" in data
    assert "id" in data
