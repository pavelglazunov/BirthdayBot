from sqlalchemy import Column, Date, String, ForeignKey, Integer

from src.models.base import Base


class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_user = Column(ForeignKey("users.telegram_id"))
    name = Column(String())
    date = Column(Date())
