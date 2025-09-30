"""
Label service
Business logic for label management
"""
from bson import ObjectId
from typing import List, Optional

from ..repositories.label_repository import LabelRepository
from ..models.label import LabelCreate, LabelUpdate, LabelResponse


class LabelService:
    """Service for label operations"""
    
    def __init__(self, label_repository: LabelRepository):
        self.label_repo = label_repository
    
    async def create_label(self, owner_id: str, label_data: LabelCreate) -> LabelResponse:
        """Create a new label"""
        label = await self.label_repo.create_label(label_data.name, ObjectId(owner_id))
        return LabelResponse(**label.model_dump())
    
    async def get_labels_by_owner(self, owner_id: str) -> List[LabelResponse]:
        """Get all labels for a user (alphabetically sorted)"""
        labels = await self.label_repo.find_by_owner(ObjectId(owner_id))
        return [LabelResponse(**label.model_dump()) for label in labels]
    
    async def update_label(
        self,
        label_id: str,
        owner_id: str,
        label_data: LabelUpdate
    ) -> Optional[LabelResponse]:
        """Update a label"""
        label = await self.label_repo.update_label(
            ObjectId(label_id),
            ObjectId(owner_id),
            label_data.name
        )
        return LabelResponse(**label.model_dump()) if label else None
    
    async def delete_label(self, label_id: str, owner_id: str) -> bool:
        """Delete a label (cascades to tasks)"""
        return await self.label_repo.delete_label(
            ObjectId(label_id),
            ObjectId(owner_id)
        )
