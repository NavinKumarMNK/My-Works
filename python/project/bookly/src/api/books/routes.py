from fastapi import APIRouter
from .schemas import Book

book_router = APIRouter()


@book_router.get("/")
async def get_all_books():
    """Get all books."""
    return {"message": "Need to get implemented"}
