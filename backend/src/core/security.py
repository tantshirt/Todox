"""
Security utilities
Password hashing and JWT token management
"""
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from .config import settings

# Bcrypt password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        user_id: User ID to encode in token
        expires_delta: Custom expiration time (default: from settings.JWT_EXPIRES_IN)
        
    Returns:
        Encoded JWT token string
    """
    from calendar import timegm
    
    if expires_delta is None:
        expires_delta = timedelta(seconds=settings.JWT_EXPIRES_IN)
    
    now = datetime.utcnow()
    expire = now + expires_delta
    
    payload = {
        "sub": user_id,
        "exp": timegm(expire.utctimetuple()),
        "iat": timegm(now.utctimetuple())
    }
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
