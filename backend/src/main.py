"""
Todox Backend API
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Todox API",
    description="Task management API with labels and priorities",
    version="1.0.0"
)

# CORS middleware configuration
# Will be properly configured with environment variables in later stories
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Will use CORS_ORIGINS env var later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Todox API - Use /docs for API documentation"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
