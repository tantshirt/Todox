"""
Label routes
Endpoints for label management
"""
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ...core.database import get_database
from ...repositories.label_repository import LabelRepository
from ...services.label_service import LabelService
from ...schemas.label import LabelCreate, LabelUpdate, LabelResponse
from ...models.user import UserInDB
from ...middleware.auth_middleware import get_current_user


router = APIRouter(prefix="/labels", tags=["labels"], redirect_slashes=False)


def get_label_service(db=Depends(get_database)) -> LabelService:
    """Dependency to get LabelService instance"""
    return LabelService(LabelRepository(db))


@router.get(
    "/",
    response_model=List[LabelResponse],
    summary="Get all labels",
    description="Get all labels for the authenticated user (alphabetically sorted)"
)
async def get_labels(
    current_user: UserInDB = Depends(get_current_user),
    label_service: LabelService = Depends(get_label_service)
):
    """Get all labels for the current user (sorted alphabetically)"""
    return await label_service.get_labels_by_owner(current_user.id)


@router.post(
    "/",
    response_model=LabelResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new label",
    description="Create a new label with unique name per user"
)
async def create_label(
    label_data: LabelCreate,
    current_user: UserInDB = Depends(get_current_user),
    label_service: LabelService = Depends(get_label_service)
):
    """
    Create a new label
    
    - **name**: Label name (1-50 characters, must be unique for your account)
    """
    return await label_service.create_label(current_user.id, label_data)


@router.patch(
    "/{label_id}",
    response_model=LabelResponse,
    summary="Update a label",
    description="Update a label's name"
)
async def update_label(
    label_id: str,
    label_data: LabelUpdate,
    current_user: UserInDB = Depends(get_current_user),
    label_service: LabelService = Depends(get_label_service)
):
    """
    Update a label's name
    
    Returns 404 if not found or not owned by user
    """
    updated_label = await label_service.update_label(label_id, current_user.id, label_data)
    
    if not updated_label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    return updated_label


@router.delete(
    "/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a label",
    description="Delete a label and remove from all tasks"
)
async def delete_label(
    label_id: str,
    current_user: UserInDB = Depends(get_current_user),
    label_service: LabelService = Depends(get_label_service)
):
    """
    Delete a label
    
    Also removes the label from all tasks' label_ids arrays (cascade delete)
    """
    deleted = await label_service.delete_label(label_id, current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
