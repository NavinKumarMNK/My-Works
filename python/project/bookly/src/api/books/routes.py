import uuid

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.api.auth import AccessTokenBearer
from .service import BookService
from .schemas import Book, BookUpdateModel, BookCreateModel, BookResponseModel

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@book_router.get(
    "/", 
    response_model=BookResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
):
    """Get all books."""
    books = await book_service.get_all_books(session)
    return {
        "message": f"Retrieved {len(books)} books",
        "data": books,
    }


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponseModel,
)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
):
    new_book = await book_service.create_book(book_data, session)
    return {
        "message": "Book Entry created successfully",
        "data": new_book
    }


@book_router.get(
    "/{book_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponseModel,
)
async def get_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)  
):
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with uuid={str(book_uid)} not found"
        )

    return {
        "message": f"{book.uid} Retrieved Successfully",
        "data": book,
    }


@book_router.patch(
    "/{book_uid}",
    status_code=status.HTTP_200_OK,
    response_model=BookResponseModel
)
async def update_book(
    book_uid: uuid.UUID,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with uuid={str(book_uid)} not found"
        )

    return {
        "message": f"{updated_book.uid} Updated Successfully",
        "data": updated_book,
    }


@book_router.delete(
    "/{book_uid}", 
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if not book_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with uuid={str(book_uid)} not found"
        )

    return {
        "message": f"Book Deleted {book_to_delete.uid}"
    }
