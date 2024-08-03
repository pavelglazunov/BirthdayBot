from aiogram import filters, Router, types, F

from src.keyboards import edit_keyboard
from src.keyboards import pagination
from src.repo import DB
from src.services import dates, aio

router = Router()


@router.message(filters.Command("birthdays"))
@router.callback_query(pagination.PaginationToMenuCallback.filter(F.name == "edit"))
async def start(message: types.Message, db: DB):
    if isinstance(message, types.CallbackQuery):
        message = message.message
        await aio.delete_message(message.bot, message.chat.id, message.message_id)

    user_id = message.chat.id
    search_ids = [user_id] + await db.group.get_by_user(user_id)

    user_birthdays = await db.birthday.get_by_ids(search_ids)
    msg = "Ваши дни рождения:\n\n"
    for birthday in user_birthdays:
        msg += f"{dates.to_text(birthday.date)} -- {birthday.name}\n"

    await message.answer(msg, reply_markup=edit_keyboard)
