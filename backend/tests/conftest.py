"""
Pytest configuration and fixtures
"""
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.core.config import settings
from src.core import database


@pytest_asyncio.fixture
async def test_db():
    """Provide test database instance"""
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[f"{settings.DATABASE_NAME}_test"]
    
    # Create indexes for test database
    from src.repositories.user_repository import UserRepository
    from src.repositories.task_repository import TaskRepository
    from src.repositories.label_repository import LabelRepository
    
    await UserRepository(db).ensure_indexes()
    await TaskRepository(db).ensure_indexes()
    await LabelRepository(db).ensure_indexes()
    
    yield db
    
    # Cleanup after tests
    await client.drop_database(f"{settings.DATABASE_NAME}_test")
    client.close()


@pytest_asyncio.fixture
async def async_client(test_db):
    """Provide async HTTP client for API testing with database initialized"""
    # Initialize database client for testing
    database.client = AsyncIOMotorClient(settings.MONGODB_URI)
    
    # Override get_database to use test database
    from src.core.database import get_database
    
    def override_get_database():
        return test_db
    
    app.dependency_overrides[get_database] = override_get_database
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as client:
        yield client
    
    # Cleanup
    app.dependency_overrides.clear()
    if database.client:
        database.client.close()
        database.client = None
