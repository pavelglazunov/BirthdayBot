from sqlalchemy.ext.asyncio import AsyncSession

from src.repo.birthday import BirthdayRepo
from src.repo.group import GroupRepo
from src.repo.user import UserRepo


class DB:
    def __init__(self, session: AsyncSession):
        self.birthday = BirthdayRepo(session)
        self.group = GroupRepo(session)
        self.user = UserRepo(session)
