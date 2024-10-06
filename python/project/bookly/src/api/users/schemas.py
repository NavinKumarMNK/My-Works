from pydantic import BaseModel, Field
from .models import User


class UserCreateModel(BaseModel):
    """CreateView for the User"""
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserResponseModel(BaseModel):
    """Response Model for the User API"""
    message: str
    data: User


class UserLoginModel(BaseModel):
    email: str
    password: str