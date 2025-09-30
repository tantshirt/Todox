"""
Label API schemas
Request and response models for label endpoints
"""
from ..models.label import LabelCreate, LabelUpdate, LabelResponse

# Re-export schemas for API use
__all__ = ['LabelCreate', 'LabelUpdate', 'LabelResponse']
