from aiogram import F, filters, Router, types

from src.filters import InPrivate

router = Router()


@router.message(filters.CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать в бота! Чтобы добавить день рождения, "
                         "воспользуйтесь командной /add")
