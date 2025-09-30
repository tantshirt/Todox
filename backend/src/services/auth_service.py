"""
Authentication service
Business logic for user registration and login
"""
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..repositories.user_repository import UserRepository
from ..models.user import UserResponse
from ..schemas.auth import TokenResponse
from ..core.security import hash_password, verify_password, create_access_token
from ..core.config import settings


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
    
    async def register_user(self, email: str, password: str) -> UserResponse:
        """
        Register a new user
        
        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            
        Returns:
            UserResponse with user data (excludes password)
            
        Raises:
            HTTPException 409: Email already registered
        """
        # Check if email already exists
        existing_user = await self.user_repo.find_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user
        try:
            user = await self.user_repo.create_user(email, hashed_password)
        except DuplicateKeyError:
            # Race condition: email was registered between check and insert
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Return user response (excludes hashed_password)
        return UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    async def login(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate user and generate JWT token
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            TokenResponse with JWT access token
            
        Raises:
            HTTPException 401: Invalid credentials (email or password)
        """
        # Find user by email
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Generate JWT token
        access_token = create_access_token(user.id)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRES_IN
        )
