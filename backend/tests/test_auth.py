"""
Authentication endpoint tests
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from jose import jwt

from src.core.config import settings
from src.core.security import hash_password
from src.repositories.user_repository import UserRepository


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


# Fixtures for login tests
@pytest_asyncio.fixture
async def test_user(test_db):
    """Create a test user for authentication tests"""
    user_repo = UserRepository(test_db)
    return await user_repo.create_user(
        email="testuser@example.com",
        hashed_password=hash_password("password123")
    )


# Login tests
@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, test_user):
    """Test successful login returns JWT token"""
    response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 3600


@pytest.mark.asyncio
async def test_login_invalid_email(async_client: AsyncClient):
    """Test login with non-existent email returns 401"""
    response = await async_client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_incorrect_password(async_client: AsyncClient, test_user):
    """Test login with wrong password returns 401"""
    response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_jwt_structure(async_client: AsyncClient, test_user):
    """Test JWT token has correct structure and fields"""
    response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Decode and verify JWT structure
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    
    assert "sub" in payload
    assert "exp" in payload
    assert "iat" in payload
    assert payload["sub"] == test_user.id


@pytest.mark.asyncio
async def test_jwt_expiry(async_client: AsyncClient, test_user):
    """Test JWT has expiry field and it's in the future"""
    from datetime import datetime
    
    response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    
    token = response.json()["access_token"]
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    
    # Verify exp field exists and is in the future
    now = datetime.utcnow().timestamp()
    assert "exp" in payload
    assert isinstance(payload["exp"], (int, float))
    assert payload["exp"] > now


@pytest.mark.asyncio
async def test_token_signature_valid(async_client: AsyncClient, test_user):
    """Test JWT token can be decoded with correct secret"""
    response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    
    token = response.json()["access_token"]
    
    # This will raise exception if signature is invalid
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    
    assert payload is not None
