"""
Security utilities
Password hashing and JWT token management
"""
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from .config import settings


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    # Convert password to bytes and hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for MongoDB storage
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


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
