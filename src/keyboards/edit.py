from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, CallbackData

from .pagination import PaginationCallbackData


class EditCallbackData(CallbackData, prefix="edit"):
    action: str
    id: int


edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Редактировать",
            callback_data=PaginationCallbackData(
                name="edit",
                offset=0,
                limit=5,
            ).pack(),
        )
    ]
])


def edit_menu_keyboard(birthday_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Заполнить заново",
                callback_data=EditCallbackData(action="rewrite", id=birthday_id).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Удалить",
                callback_data=EditCallbackData(action="delete", id=birthday_id).pack(),
            )
        ],
    ])
