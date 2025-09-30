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


# JWT Middleware tests
@pytest.mark.asyncio
async def test_get_me_with_valid_token(async_client: AsyncClient, test_user):
    """Test GET /auth/me with valid token returns user info"""
    # Login to get token
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Call /auth/me with token
    response = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["id"] == test_user.id
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_get_me_without_token(async_client: AsyncClient):
    """Test GET /auth/me without token returns 401"""
    response = await async_client.get("/auth/me")
    
    assert response.status_code == 403  # HTTPBearer returns 403 for missing auth


@pytest.mark.asyncio
async def test_get_me_with_invalid_token(async_client: AsyncClient):
    """Test GET /auth/me with malformed token returns 401"""
    response = await async_client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token-string"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_wrong_signature(async_client: AsyncClient, test_user):
    """Test GET /auth/me with token signed by wrong secret returns 401"""
    # Create token with different secret
    wrong_token = jwt.encode(
        {"sub": test_user.id, "exp": 9999999999},
        "wrong-secret-key",
        algorithm=settings.JWT_ALGORITHM
    )
    
    response = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {wrong_token}"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_expired_token(async_client: AsyncClient, test_user):
    """Test GET /auth/me with expired token returns 401"""
    from datetime import datetime, timedelta
    from calendar import timegm
    
    # Create expired token (expired 1 hour ago)
    past_time = datetime.utcnow() - timedelta(hours=1)
    expired_payload = {
        "sub": test_user.id,
        "exp": timegm(past_time.utctimetuple()),
        "iat": timegm(past_time.utctimetuple())
    }
    expired_token = jwt.encode(
        expired_payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    response = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    assert response.status_code == 401


# Integration test for complete auth flow
@pytest.mark.asyncio
async def test_complete_auth_flow(async_client: AsyncClient, test_db):
    """Test complete authentication flow: register → login → access protected route"""
    # Step 1: Register a new user
    register_response = await async_client.post(
        "/auth/register",
        json={"email": "flowtest@example.com", "password": "testpass123"}
    )
    assert register_response.status_code == 201
    registered_user = register_response.json()
    
    # Step 2: Login with registered credentials
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "flowtest@example.com", "password": "testpass123"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    
    # Step 3: Access protected route with token
    me_response = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"}
    )
    assert me_response.status_code == 200
    user_data = me_response.json()
    
    # Step 4: Verify user data matches
    assert user_data["email"] == "flowtest@example.com"
    assert user_data["id"] == registered_user["id"]
