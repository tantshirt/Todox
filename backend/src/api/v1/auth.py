"""
Authentication routes
Endpoints for user registration and login
"""
from fastapi import APIRouter, Depends, status

from ...core.database import get_database
from ...repositories.user_repository import UserRepository
from ...services.auth_service import AuthService
from ...schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UpdatePasswordRequest
from ...models.user import UserResponse, UserInDB
from ...middleware.auth_middleware import get_current_user


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


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get authenticated user's information"
)
async def get_current_user_info(
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.patch(
    "/update-password",
    status_code=status.HTTP_200_OK,
    summary="Update user password",
    description="Change user password after verifying current password"
)
async def update_password(
    data: UpdatePasswordRequest,
    current_user: UserInDB = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Update user password
    
    - **current_password**: Current password for verification
    - **new_password**: New password (minimum 8 characters)
    
    Requires valid JWT token in Authorization header
    """
    await auth_service.update_password(
        current_user.id,
        data.current_password,
        data.new_password
    )
    return {"message": "Password updated successfully"}
