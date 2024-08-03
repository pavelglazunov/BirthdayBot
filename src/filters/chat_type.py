from aiogram import types
from aiogram.filters import BaseFilter


class InPrivate(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        return message.chat.type == "private"


class InGroup(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        return message.chat.type in ("group", "supergroup")
