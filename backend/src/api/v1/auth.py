"""
Authentication routes
Endpoints for user registration and login
"""
from fastapi import APIRouter, Depends, status

from ...core.database import get_database
from ...repositories.user_repository import UserRepository
from ...services.auth_service import AuthService
from ...schemas.auth import RegisterRequest
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
