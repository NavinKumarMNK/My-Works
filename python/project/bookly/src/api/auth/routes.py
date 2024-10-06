from fastapi import APIRouter

from .service import AuthService

auth_router = APIRouter()
auth_service = AuthService()

