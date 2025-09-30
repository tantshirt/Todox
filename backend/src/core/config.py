"""
Application configuration
Loads environment variables using Pydantic Settings
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    model_config = ConfigDict(env_file=".env", case_sensitive=True)
    
    MONGODB_URI: str
    DATABASE_NAME: str = "todox"
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_EXPIRES_IN: int = 3600
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: str = "http://localhost:3000"


settings = Settings()
