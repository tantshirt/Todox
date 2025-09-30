"""
Task data models
Pydantic models for task entities
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime, date

TaskPriority = Literal['High', 'Medium', 'Low']
TaskStatus = Literal['open', 'done']


class TaskBase(BaseModel):
    """Base task model with shared fields"""
    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")
    priority: TaskPriority = Field(..., description="Task priority: High, Medium, or Low")
    deadline: date = Field(..., description="Task deadline (ISO 8601 date)")


class TaskCreate(TaskBase):
    """Schema for task creation"""
    label_ids: List[str] = Field(default_factory=list, description="Label IDs to assign")


class TaskUpdate(BaseModel):
    """Schema for task updates (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[date] = None
    status: Optional[TaskStatus] = None
    label_ids: Optional[List[str]] = None


class TaskInDB(TaskBase):
    """Task model as stored in database"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    status: TaskStatus = 'open'
    label_ids: List[str] = Field(default_factory=list)
    owner_id: str
    created_at: datetime
    updated_at: datetime


# Alias for API responses
TaskResponse = TaskInDB
