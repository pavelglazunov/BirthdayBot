from typing import Sequence, Union

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Group


class GroupRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, chat_id: int) -> Union[Group, None]:
        group = Group(
            group_id=chat_id,
            user_id=user_id,
        )
        try:
            self.session.add(group)
            await self.session.commit()

            return group
        except IntegrityError:
            await self.session.rollback()

            return None

    async def get_by_user(self, user_id: int) -> Sequence[Group]:
        return (await self.session.scalars(select(Group.group_id).filter(
            Group.user_id == user_id,
        ))).all()
