"""
Label repository
Database operations for label entities
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status

from ..models.label import LabelInDB


class LabelRepository:
    """Repository for label database operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.labels
        self.tasks_collection = db.tasks
    
    async def create_label(self, name: str, owner_id: ObjectId) -> LabelInDB:
        """
        Create a new label
        
        Args:
            name: Label name
            owner_id: User's ObjectId
            
        Returns:
            LabelInDB: Created label
            
        Raises:
            HTTPException 409: Label name already exists for this user
        """
        label_data = {
            "name": name,
            "owner_id": owner_id,
            "created_at": datetime.utcnow()
        }
        
        try:
            result = await self.collection.insert_one(label_data)
            label_data["_id"] = result.inserted_id
            return LabelInDB(**self._doc_to_dict(label_data))
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Label '{name}' already exists"
            )
    
    async def find_by_owner(self, owner_id: ObjectId) -> List[LabelInDB]:
        """
        Find all labels for a user, sorted alphabetically
        
        Args:
            owner_id: User's ObjectId
            
        Returns:
            List of LabelInDB (alphabetically sorted)
        """
        cursor = self.collection.find({'owner_id': owner_id}).sort('name', 1)
        labels = await cursor.to_list(length=None)
        return [LabelInDB(**self._doc_to_dict(label)) for label in labels]
    
    async def find_by_id(self, label_id: ObjectId, owner_id: ObjectId) -> Optional[LabelInDB]:
        """
        Find a label by ID with ownership verification
        
        Args:
            label_id: Label's ObjectId
            owner_id: User's ObjectId
            
        Returns:
            LabelInDB if found and owned, None otherwise
        """
        label = await self.collection.find_one({'_id': label_id, 'owner_id': owner_id})
        return LabelInDB(**self._doc_to_dict(label)) if label else None
    
    async def update_label(
        self,
        label_id: ObjectId,
        owner_id: ObjectId,
        name: str
    ) -> Optional[LabelInDB]:
        """
        Update a label's name
        
        Args:
            label_id: Label's ObjectId
            owner_id: User's ObjectId
            name: New label name
            
        Returns:
            Updated LabelInDB or None if not found/not owned
            
        Raises:
            HTTPException 409: New name conflicts with existing label
        """
        try:
            result = await self.collection.find_one_and_update(
                {'_id': label_id, 'owner_id': owner_id},
                {'$set': {'name': name}},
                return_document=True
            )
            return LabelInDB(**self._doc_to_dict(result)) if result else None
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Label '{name}' already exists"
            )
    
    async def delete_label(self, label_id: ObjectId, owner_id: ObjectId) -> bool:
        """
        Delete a label and remove from all tasks
        
        Args:
            label_id: Label's ObjectId
            owner_id: User's ObjectId
            
        Returns:
            True if deleted, False if not found/not owned
        """
        # First verify label exists and is owned
        label = await self.find_by_id(label_id, owner_id)
        if not label:
            return False
        
        # Remove label from all tasks (cascade delete)
        await self.remove_label_from_tasks(label_id, owner_id)
        
        # Delete the label
        result = await self.collection.delete_one({'_id': label_id, 'owner_id': owner_id})
        return result.deleted_count > 0
    
    async def remove_label_from_tasks(self, label_id: ObjectId, owner_id: ObjectId):
        """
        Remove a label ID from all tasks' label_ids arrays
        
        Args:
            label_id: Label ObjectId to remove
            owner_id: User's ObjectId (for safety)
        """
        label_id_str = str(label_id)
        
        await self.tasks_collection.update_many(
            {
                'owner_id': owner_id,
                'label_ids': label_id_str
            },
            {
                '$pull': {'label_ids': label_id_str}
            }
        )
    
    async def ensure_indexes(self):
        """Create required indexes for labels collection"""
        # Compound unique index: (owner_id, name)
        # Prevents duplicate label names per user
        await self.collection.create_index(
            [("owner_id", 1), ("name", 1)],
            unique=True
        )
    
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
        return doc
