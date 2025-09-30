"""
Task routes
Endpoints for task management
"""
from fastapi import APIRouter, Depends, status
from typing import List

from ...core.database import get_database
from ...repositories.task_repository import TaskRepository
from ...services.task_service import TaskService
from ...schemas.task import TaskCreate, TaskResponse
from ...models.user import UserInDB
from ...middleware.auth_middleware import get_current_user


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db=Depends(get_database)) -> TaskService:
    """Dependency to get TaskService instance"""
    return TaskService(TaskRepository(db))


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with title, priority, and deadline"
)
async def create_task(
    task_data: TaskCreate,
    current_user: UserInDB = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Create a new task
    
    - **title**: Task title (1-200 characters, required)
    - **description**: Optional description
    - **priority**: High, Medium, or Low (required)
    - **deadline**: ISO 8601 date (required)
    - **label_ids**: Optional array of label IDs
    
    Returns the created task with id, status (defaults to 'open'), and timestamps
    """
    return await task_service.create_task(current_user.id, task_data)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Get all tasks",
    description="Get all tasks for the authenticated user"
)
async def get_tasks(
    current_user: UserInDB = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get all tasks for the current user
    
    Returns array of tasks sorted by created_at (newest first).
    Returns empty array if user has no tasks.
    """
    return await task_service.get_tasks_by_owner(current_user.id)
