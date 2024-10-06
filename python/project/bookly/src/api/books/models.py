import uuid
import sqlalchemy.dialects.postgresql as pg

from datetime import datetime, date
from sqlmodel import SQLModel, Field, Column


class Book(SQLModel, table=True):
    """Base Model to represent a Book Table in Postgres"""
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,   # using pg dialects to say the type of this column
            nullable=False,  # this column cant be null
            primary_key=True,  # set this column as primary key
            default=uuid.uuid4  # generate a new uuid
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=datetime.now
        )
    )

    def __repr__(self):
        return f"<Book {self.title}>"
