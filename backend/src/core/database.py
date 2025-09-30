"""
MongoDB database connection
Provides async MongoDB client using Motor
"""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings

# Global client instance
client: Optional[AsyncIOMotorClient] = None


async def connect_to_database():
    """Initialize MongoDB connection on startup"""
    global client
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        maxPoolSize=10,
        minPoolSize=1
    )
    
    # Test connection
    await client.admin.command('ping')
    print(f"Connected to MongoDB database: {settings.DATABASE_NAME}")
    
    # Create indexes
    from ..repositories.user_repository import UserRepository
    from ..repositories.task_repository import TaskRepository
    from ..repositories.label_repository import LabelRepository
    db = get_database()
    
    user_repo = UserRepository(db)
    await user_repo.ensure_indexes()
    
    task_repo = TaskRepository(db)
    await task_repo.ensure_indexes()
    
    label_repo = LabelRepository(db)
    await label_repo.ensure_indexes()
    
    print("Database indexes created")


async def close_database_connection():
    """Close MongoDB connection on shutdown"""
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_database() -> AsyncIOMotorDatabase:
    """
    Dependency function that returns the database instance
    Used in FastAPI route dependencies
    """
    if client is None:
        raise RuntimeError("Database not initialized")
    return client[settings.DATABASE_NAME]
