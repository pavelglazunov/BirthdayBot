from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.keyboards import EditCallbackData, cancel_keyboard
from src.keyboards import pagination, edit_menu_keyboard, EditCallbackData
from src.repo import DB
from src.services import dates
from src.states import BirthdayState

router = Router()


@router.callback_query(pagination.PaginationCallbackData.filter(F.name == "edit"))
async def show_birthdays(
        callback: types.CallbackQuery,
        callback_data: pagination.PaginationCallbackData,
        db: DB,
):
    birthdays = await db.birthday.get_by_ids([callback.message.chat.id])
    await callback.message.edit_text(
        text="Укажите день рождения:",
        reply_markup=pagination.pagination_keyboard(
            name=callback_data.name,
            offset=callback_data.offset,
            limit=callback_data.limit,
            buttons_text=[b.name for b in birthdays],
            buttons_callback=[str(b.id) for b in birthdays],
            add_back_button=True,
        ),
    )


@router.callback_query(pagination.PaginationSelectCallbackData.filter(F.name == "edit"))
async def select_birthday(
        callback: types.CallbackQuery,
        callback_data: pagination.PaginationSelectCallbackData,
        db: DB,
):
    await callback.message.edit_text(
        text="Выберите действие:",
        reply_markup=pagination.pagination_select_back(
            base_keyboard=edit_menu_keyboard(int(callback_data.value)),
            name=callback_data.name,
            offset=callback_data.offset,
            limit=callback_data.limit,
        )
    )


@router.callback_query(EditCallbackData.filter(F.action == "delete"))
async def delete_birthday(
        callback: types.CallbackQuery,
        callback_data: EditCallbackData,
        db: DB,
):
    await db.birthday.delete(callback_data.id)
    await callback.message.edit_text("День рождения успешно удален!", reply_markup=None)


@router.callback_query(EditCallbackData.filter(F.action == "rewrite"))
async def edit_birthday(
        callback: types.CallbackQuery,
        callback_data: EditCallbackData,
        state: FSMContext,
):
    await state.update_data(user_id=callback.message.from_user.id)
    await state.update_data(update_id=callback_data.id)

    await state.set_state(BirthdayState.data)
    await callback.message.edit_text(
        text="Отлично, введите имя и дату рождения, как в примере ниже\n\n"
             "<i>Вася Иванов (@username), 1 января</i>\n\n"
             "P.S. юзернем указывать не обязательно, но так вам будет проще найти "
             "человека в его день рождения",
        reply_markup=cancel_keyboard,
    )
