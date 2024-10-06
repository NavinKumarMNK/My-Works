from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book
import uuid

class BookService():
    async def get_all_books(self, session: AsyncSession):
        _statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(_statement)
        return result.all()

    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        _statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(_statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_uid: uuid.UUID, book_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update:
            return None

        update_data_dict = book_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)

        await session.commit()
        return book_to_update

    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if not book_to_delete:
            return None

        await session.delete(book_to_delete)
        await session.commit()
        return book_to_delete
