"""
Authentication middleware
JWT token verification and user authentication
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import JWTError, jwt
from bson import ObjectId

from ..core.config import settings
from ..core.database import get_database
from ..repositories.user_repository import UserRepository
from ..models.user import UserInDB

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_database)
) -> UserInDB:
    """
    FastAPI dependency that verifies JWT token and returns current user.
    
    Extracts token from Authorization header, decodes and validates it,
    then fetches the user from the database.
    
    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database instance from dependency
        
    Returns:
        UserInDB: Authenticated user
        
    Raises:
        HTTPException 401: Invalid, expired, or missing token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract user_id from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    user_repo = UserRepository(db)
    user = await user_repo.find_by_id(ObjectId(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user
