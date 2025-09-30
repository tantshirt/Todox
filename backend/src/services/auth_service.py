"""
Authentication service
Business logic for user registration and login
"""
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..repositories.user_repository import UserRepository
from ..models.user import UserResponse
from ..core.security import hash_password


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
