import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    """Model for Reviews"""
    uid: uuid.UUID
    rating: int = Field(le=5, gt=0)
    review_text: str
    user_uid: uuid.UUID
    book_uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    """CreateView for Reviews"""
    rating: int = Field(le=5, gt=0)
    review_text: str
