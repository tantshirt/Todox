"""
Task repository
Database operations for task entities
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

from ..models.task import TaskInDB


class TaskRepository:
    """Repository for task database operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks
    
    async def create_task(self, task_data: dict) -> TaskInDB:
        """
        Create a new task in the database
        
        Args:
            task_data: Task data dictionary
            
        Returns:
            TaskInDB: Created task with id and timestamps
        """
        # Convert date to datetime for MongoDB storage
        if 'deadline' in task_data and hasattr(task_data['deadline'], 'isoformat'):
            task_data['deadline'] = datetime.combine(task_data['deadline'], datetime.min.time())
        
        task_data['created_at'] = datetime.utcnow()
        task_data['updated_at'] = datetime.utcnow()
        task_data['status'] = task_data.get('status', 'open')
        task_data['label_ids'] = task_data.get('label_ids', [])
        
        result = await self.collection.insert_one(task_data)
        task_data['_id'] = result.inserted_id
        
        return TaskInDB(**self._doc_to_dict(task_data))
    
    async def find_by_owner(self, owner_id: ObjectId) -> List[TaskInDB]:
        """
        Find all tasks belonging to a user, sorted by created_at descending
        
        Args:
            owner_id: User's ObjectId
            
        Returns:
            List of TaskInDB (newest first)
        """
        cursor = self.collection.find({'owner_id': owner_id}).sort('created_at', -1)
        tasks = await cursor.to_list(length=None)
        return [TaskInDB(**self._doc_to_dict(task)) for task in tasks]
    
    async def find_by_id(self, task_id: ObjectId, owner_id: ObjectId) -> Optional[TaskInDB]:
        """
        Find a task by ID, ensuring it belongs to the owner
        
        CRITICAL: Always includes owner_id in query for security
        
        Args:
            task_id: Task's ObjectId
            owner_id: User's ObjectId
            
        Returns:
            TaskInDB if found and owned by user, None otherwise
        """
        task = await self.collection.find_one({'_id': task_id, 'owner_id': owner_id})
        return TaskInDB(**self._doc_to_dict(task)) if task else None
    
    async def update_task(
        self, 
        task_id: ObjectId, 
        owner_id: ObjectId, 
        update_data: dict
    ) -> Optional[TaskInDB]:
        """
        Update a task's fields
        
        CRITICAL: Always includes owner_id in query for security
        
        Args:
            task_id: Task's ObjectId
            owner_id: User's ObjectId
            update_data: Fields to update
            
        Returns:
            Updated TaskInDB if found and owned by user, None otherwise
        """
        # Convert date to datetime for MongoDB storage
        if 'deadline' in update_data and hasattr(update_data['deadline'], 'isoformat'):
            update_data['deadline'] = datetime.combine(update_data['deadline'], datetime.min.time())
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {'_id': task_id, 'owner_id': owner_id},
            {'$set': update_data},
            return_document=True
        )
        
        return TaskInDB(**self._doc_to_dict(result)) if result else None
    
    async def delete_task(self, task_id: ObjectId, owner_id: ObjectId) -> bool:
        """
        Delete a task
        
        CRITICAL: Always includes owner_id in query for security
        
        Args:
            task_id: Task's ObjectId
            owner_id: User's ObjectId
            
        Returns:
            True if task was deleted, False if not found or not owned by user
        """
        result = await self.collection.delete_one({'_id': task_id, 'owner_id': owner_id})
        return result.deleted_count > 0
    
    async def ensure_indexes(self):
        """Create required indexes for tasks collection"""
        # Index for filtering by owner
        await self.collection.create_index("owner_id")
        
        # Compound index for sorted queries by owner
        await self.collection.create_index([("owner_id", 1), ("created_at", -1)])
    
    def _doc_to_dict(self, doc: dict) -> dict:
        """
        Convert MongoDB document to dict with string ids
        
        Args:
            doc: MongoDB document
            
        Returns:
            Dictionary with _id and owner_id converted to strings
        """
        if doc and '_id' in doc:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        if 'owner_id' in doc and isinstance(doc['owner_id'], ObjectId):
            doc['owner_id'] = str(doc['owner_id'])
        # Convert label_ids ObjectIds to strings if necessary
        if 'label_ids' in doc and doc['label_ids']:
            doc['label_ids'] = [str(lid) if isinstance(lid, ObjectId) else lid 
                               for lid in doc['label_ids']]
        # Convert datetime back to date for deadline
        if 'deadline' in doc and isinstance(doc['deadline'], datetime):
            doc['deadline'] = doc['deadline'].date()
        return doc
