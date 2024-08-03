from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, telegram_id: int) -> Union[User, None]:
        return await self.session.scalar(select(User).filter(User.telegram_id == telegram_id))

    async def create(self, telegram_id: int, telegram_username: str) -> User:
        user = User(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
        )

        self.session.add(user)
        await self.session.commit()

        return user

    async def update(self, user: User, **kwargs):
        for k, v in kwargs.items():
            setattr(user, k, v)

        await self.session.commit()
