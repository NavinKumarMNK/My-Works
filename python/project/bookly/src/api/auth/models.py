import uuid
import sqlalchemy.dialects.postgresql as pg

from sqlmodel import SQLModel, Field, Column
from datetime import datetime


class User(SQLModel, table=True):
    """Base Model to represent a Users Table in Postgres"""
    __tablename__ = 'users'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
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
        return f"<User {self.username}>"
