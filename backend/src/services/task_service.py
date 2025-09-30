"""
Task service
Business logic for task management
"""
from bson import ObjectId

from ..repositories.task_repository import TaskRepository
from ..models.task import TaskCreate, TaskResponse


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
