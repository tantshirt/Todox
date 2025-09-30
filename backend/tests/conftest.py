"""
Pytest configuration and fixtures
"""
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.core.config import settings


@pytest_asyncio.fixture
async def test_db():
    """Provide test database instance"""
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[f"{settings.DATABASE_NAME}_test"]
    
    yield db
    
    # Cleanup after tests
    await client.drop_database(f"{settings.DATABASE_NAME}_test")
    client.close()


@pytest_asyncio.fixture
async def async_client():
    """Provide async HTTP client for API testing"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
