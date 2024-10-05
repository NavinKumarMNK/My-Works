import uuid
from datetime import datetime
from pydantic import BaseModel


class TagModel(BaseModel):
    """Model to define Tags"""
    uid: uuid.UUID
    name: str
    created_at: datetime


class TagCreateModel(BaseModel):
    """Create View for Tags"""
    name: str
