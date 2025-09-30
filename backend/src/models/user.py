"""
User data models
Pydantic models for user entities
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with shared fields"""
    email: EmailStr


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters")


class UserInDB(UserBase):
    """User model as stored in database"""
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """User model for API responses (excludes password)"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
