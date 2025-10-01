"""
Todox Backend API
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.database import connect_to_database, close_database_connection
from .core.config import settings
from .api.v1 import auth, tasks, labels


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await connect_to_database()
    yield
    # Shutdown
    await close_database_connection()


app = FastAPI(
    title="Todox API",
    description="Task management API with labels and priorities",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(labels.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Todox API - Use /docs for API documentation"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Verifies API is running and database is connected
    """
    try:
        # Ping database to verify connection
        from .core.database import client
        if client:
            await client.admin.command('ping')
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "not initialized"}, 503
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}, 503
