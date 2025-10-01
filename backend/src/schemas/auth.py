"""
Authentication schemas
Request and response models for auth endpoints
"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Schema for user registration request"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class LoginRequest(BaseModel):
    """Schema for user login request"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiry time in seconds")


class UpdatePasswordRequest(BaseModel):
    """Schema for updating user password"""
    current_password: str = Field(..., description="Current password for verification")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
