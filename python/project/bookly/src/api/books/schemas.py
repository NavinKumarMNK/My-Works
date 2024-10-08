import uuid
from datetime import datetime, date

from pydantic import BaseModel
from src.api.reviews.schemas import ReviewModel
from src.api.tags.schemas import TagModel


class Book(BaseModel):
    """Base Model to represent a book"""
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: date
    language: str
    created_at: datetime
    updated_at: datetime


class BookDetailModel(Book):
    """Detail View for the Book"""
    reviews: list[ReviewModel]
    tags: list[TagModel]


class BookCreateModel(BaseModel):
    """CreateView for the Book"""
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: date
    language: str


class BookUpdateModel(BaseModel):
    """Update Model for the Book"""
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: date
    language: str


class BookResponseModel(BaseModel):
    """Response Model for the Book API"""
    message: str
    data: Book | list[Book]
