from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .models import User
from .schemas import UserCreateModel
from src.utils.security import generate_password_hash


class UserService():
    async def get_user_by_email(self, email, session: AsyncSession):
        _statement = select(User).where(User.email == email)
        result = await session.exec(_statement)
        user = result.first()
        return user if user is not None else None

    async def user_exists_by_email(self, email, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data: User, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict['password'])

        session.add(new_user)
        await session.commit()

        return new_user