from aiogram import Router, types

from src.filters import InGroup
from src.repo import DB

router = Router()


@router.message(InGroup())
async def all_messages(message: types.Message, db: DB):
    await db.group.create(message.from_user.id, message.chat.id)
