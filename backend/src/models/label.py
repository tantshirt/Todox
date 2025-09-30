"""
Label data models
Pydantic models for label entities
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LabelBase(BaseModel):
    """Base label model with shared fields"""
    name: str = Field(min_length=1, max_length=50, description="Label name")


class LabelCreate(LabelBase):
    """Schema for label creation"""
    pass


class LabelUpdate(LabelBase):
    """Schema for label updates"""
    pass


class LabelInDB(LabelBase):
    """Label model as stored in database"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    owner_id: str
    created_at: datetime


# Alias for API responses
LabelResponse = LabelInDB
