"""
Task service
Business logic for task management
"""
from bson import ObjectId
from typing import List, Optional

from ..repositories.task_repository import TaskRepository
from ..models.task import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    """Service for task operations"""
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repo = task_repository
    
    async def create_task(self, owner_id: str, task_data: TaskCreate) -> TaskResponse:
        """
        Create a new task for the authenticated user
        
        Args:
            owner_id: Authenticated user's ID
            task_data: Task creation data
            
        Returns:
            TaskResponse: Created task with all fields
        """
        # Convert to dict and add owner_id
        task_dict = task_data.model_dump()
        task_dict['owner_id'] = ObjectId(owner_id)
        
        # Create task in database
        task = await self.task_repo.create_task(task_dict)
        
        return TaskResponse(**task.model_dump())
    
    async def get_tasks_by_owner(self, owner_id: str) -> List[TaskResponse]:
        """
        Get all tasks for a user
        
        Args:
            owner_id: User's ID
            
        Returns:
            List of TaskResponse objects (sorted newest first)
        """
        tasks = await self.task_repo.find_by_owner(ObjectId(owner_id))
        return [TaskResponse(**task.model_dump()) for task in tasks]
    
    async def update_task(
        self,
        task_id: str,
        owner_id: str,
        task_data: TaskUpdate
    ) -> Optional[TaskResponse]:
        """
        Update a task
        
        Args:
            task_id: Task ID
            owner_id: User's ID
            task_data: Fields to update
            
        Returns:
            Updated TaskResponse or None if not found/not owned
        """
        # Convert to dict, excluding None values
        update_dict = task_data.model_dump(exclude_none=True)
        
        task = await self.task_repo.update_task(
            ObjectId(task_id),
            ObjectId(owner_id),
            update_dict
        )
        
        return TaskResponse(**task.model_dump()) if task else None
    
    async def delete_task(self, task_id: str, owner_id: str) -> bool:
        """
        Delete a task
        
        Args:
            task_id: Task ID
            owner_id: User's ID
            
        Returns:
            True if deleted, False if not found/not owned
        """
        return await self.task_repo.delete_task(
            ObjectId(task_id),
            ObjectId(owner_id)
        )
