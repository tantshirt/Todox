"""
Application configuration
Loads environment variables using Pydantic Settings
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    MONGODB_URI: str
    DATABASE_NAME: str = "todox"
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_EXPIRES_IN: int = 3600
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
