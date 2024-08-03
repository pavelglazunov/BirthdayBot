import datetime
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Birthday


class BirthdayRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, from_user_id: int, content: str, date: datetime.date) -> Birthday:
        birthday = Birthday(
            from_user=from_user_id,
            name=content,
            date=date,
        )

        self.session.add(birthday)
        await self.session.commit()

        return birthday

    async def get(self, birthday_id: int) -> Birthday:
        return await self.session.scalar(select(Birthday).filter(Birthday.id == birthday_id))

    async def update(self, birthday_id: int, **kwargs):
        birthday = self.get(birthday_id)
        for k, v in kwargs.items():
            setattr(birthday, k, v)

        await self.session.commit()

    async def get_by_ids(self, ids: list[int]) -> Sequence[Birthday]:
        return (await self.session.scalars(select(Birthday).filter(
            Birthday.from_user.in_(ids)
        ).order_by(Birthday.date))).all()

    async def delete(self, birthday_id: int):
        await self.session.execute(delete(Birthday).filter(Birthday.id == birthday_id))
        await self.session.commit()

    async def today(self):
        today = datetime.date.today()
        return (await self.session.scalars(select(Birthday).filter(Birthday.date == today))).all()
