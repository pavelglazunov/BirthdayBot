from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, CallbackData


class CreateCallbackData(CallbackData, prefix="edit"):
    pass


cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Отменить",
            callback_data=CreateCallbackData().pack(),
        )
    ]
])
