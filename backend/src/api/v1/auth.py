"""
Authentication routes
Endpoints for user registration and login
"""
from fastapi import APIRouter, Depends, status

from ...core.database import get_database
from ...repositories.user_repository import UserRepository
from ...services.auth_service import AuthService
from ...schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from ...models.user import UserResponse


router = APIRouter(prefix="/auth", tags=["authentication"])


def get_auth_service(db=Depends(get_database)) -> AuthService:
    """Dependency to get AuthService instance"""
    return AuthService(UserRepository(db))


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    
    - **email**: Valid email address (must be unique)
    - **password**: At least 8 characters
    
    Returns the created user (excludes password)
    """
    return await auth_service.register_user(data.email, data.password)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user and receive JWT access token"
)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login with email and password
    
    - **email**: User's registered email
    - **password**: User's password
    
    Returns JWT access token for authenticated requests
    """
    return await auth_service.login(data.email, data.password)
