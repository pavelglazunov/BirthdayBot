from sqlalchemy import Column, Integer, String

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    telegram_username = Column(String)
