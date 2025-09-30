"""
Task routes
Endpoints for task management
"""
from fastapi import APIRouter, Depends, status
from typing import List

from ...core.database import get_database
from ...repositories.task_repository import TaskRepository
from ...services.task_service import TaskService
from ...schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ...models.user import UserInDB
from ...middleware.auth_middleware import get_current_user
from fastapi import HTTPException


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


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update task fields (partial update supported)"
)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: UserInDB = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Update a task
    
    - **task_id**: Task ID to update
    - Any combination of: title, description, priority, deadline, status, label_ids
    
    Returns updated task or 404 if not found/not owned by user
    """
    updated_task = await task_service.update_task(task_id, current_user.id, task_data)
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task permanently"
)
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a task
    
    - **task_id**: Task ID to delete
    
    Returns 204 No Content on success, 404 if not found/not owned by user
    """
    deleted = await task_service.delete_task(task_id, current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
