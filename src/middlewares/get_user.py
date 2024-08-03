from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject

from config.config import config
from src.repo import DB
from src.services import serialise

class GetUserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        db: DB = data['db']

        user = await db.user.get(event.from_user.id)
        username = serialise.username(event.from_user.username)

        if not user:
            if not event.from_user.username:
                return await event.answer("Вам необходимо установить юзернейм в телеграме")

            user = await db.user.create(
                telegram_id=event.from_user.id,
                telegram_username=username,
            )

        if user.telegram_username != username:
            await db.user.update(user, telegram_username=event.from_user.username)

        data['user'] = user

        return await handler(event, data)
