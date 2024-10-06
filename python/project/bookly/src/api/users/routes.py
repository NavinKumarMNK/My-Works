from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime


from .schemas import UserCreateModel, UserResponseModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from src.api.auth import RefreshTokenBearer
from src.utils.security import verify_password, create_access_token

auth_router = APIRouter()
user_service = UserService()
refresh_token_bearer = RefreshTokenBearer()

@auth_router.post(
    "/signup",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists_by_email(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )

    new_user = await user_service.create_user(user_data, session)

    return {
        "message": "User Created",
        "data": new_user
    }

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user:
        is_password_valid = verify_password(password, user.password_hash)
        if is_password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                },
                expiry=timedelta(seconds=3600),
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password",
    )

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = datetime.strptime(token_details['expiry'])
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user_data'],
        )

        return JSONResponse(content={
            "message": "New Access Token Created Succesfully",
            "access_token": new_access_token,
        })
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired Refresh Token")
