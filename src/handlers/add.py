from aiogram import filters, Router, types
from aiogram.fsm.context import FSMContext

from src.keyboards import CreateCallbackData, cancel_keyboard
from src.repo import DB
from src.services import dates
from src.states import BirthdayState

router = Router()


@router.message(filters.Command("add"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Отлично, введите имя и дату рождения, как в примере ниже\n\n"
                         "<i>Вася Иванов (@username), 1 января</i>\n\n"
                         "P.S. юзернем указывать не обязательно, но так вам будет проще найти "
                         "человека в его день рождения", reply_markup=cancel_keyboard)

    await state.update_data(user_id=message.from_user.id)
    await state.set_state(BirthdayState.data)


@router.message(BirthdayState.data)
async def input_birthday(message: types.Message, state: FSMContext, db: DB):
    data = await state.get_data()
    if data.get("user_id", 0) != message.from_user.id:
        return

    content, _, date = message.text.rpartition(",")
    if not (content and date):
        await message.answer("Простите, мне не удалось понять ваш текст, попробуйте еще раз")
        return
    birthday_date, error_message = dates.from_text(date)
    if not birthday_date:
        await message.answer(error_message)
        return

    if birthday_id := data.get("update_id"):
        await db.birthday.update(
            birthday_id=birthday_id,
            content=content,
            date=birthday_date,
        )
        await message.answer("День рождения успешно добавлен!")
        await state.clear()
        return

    await db.birthday.create(
        from_user_id=message.chat.id,
        content=content,
        date=birthday_date,
    )
    await message.answer("День рождения успешно добавлен!")
    await state.clear()


@router.callback_query(CreateCallbackData().filter())
async def cancel_input(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Добавление дня рождения отменено")
