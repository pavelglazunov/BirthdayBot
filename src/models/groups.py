from sqlalchemy import Column, Integer, ForeignKey

from src.models.base import Base


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.telegram_id"), primary_key=True)
