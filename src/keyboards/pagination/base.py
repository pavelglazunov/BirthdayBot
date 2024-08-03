from aiogram.utils.keyboard import (
    CallbackData,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardBuilder,
)


class PaginationCallbackData(CallbackData, prefix="pagination"):
    name: str
    offset: int
    limit: int


class PaginationSelectCallbackData(CallbackData, prefix="pag-answer"):
    name: str
    value: str
    offset: int
    limit: int


class PaginationBackCallbackData(CallbackData, prefix="pag-back"):
    name: str


class PaginationToMenuCallback(CallbackData, prefix="pag-to-menu"):
    name: str


def pagination_keyboard(
        name: str,
        offset: int,
        limit: int,
        buttons_text: list[str],
        buttons_callback: list[str],
        add_back_button: bool = True,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for text, callback in zip(buttons_text, buttons_callback):
        builder.row(InlineKeyboardButton(
            text=text,
            callback_data=PaginationSelectCallbackData(
                name=name,
                value=callback,
                offset=offset,
                limit=limit,
            ).pack(),
        ))

    if offset > 0:
        builder.row(InlineKeyboardButton(
            text="<<<",
            callback_data=PaginationCallbackData(
                name=name,
                offset=offset - limit if offset - limit >= 0 else 0,
                limit=limit,
            ).pack(),
        ))
    if len(buttons_text) == limit:
        button = InlineKeyboardButton(
            text=">>>",
            callback_data=PaginationCallbackData(
                name=name,
                offset=offset + limit,
                limit=limit,
            ).pack(),
        )
        if offset > 0:
            builder.add(button)
        else:
            builder.row(button)

    if add_back_button:
        builder.row(InlineKeyboardButton(
            text="↩️ Назад",
            callback_data=PaginationToMenuCallback(
                name=name,
            ).pack(),
        ))

    return builder.as_markup()


def pagination_select_back(
        base_keyboard: InlineKeyboardMarkup,
        name: str,
        offset: int,
        limit: int
) -> InlineKeyboardMarkup:
    button = [InlineKeyboardButton(
        text="↩️ Назад",
        callback_data=PaginationCallbackData(
            name=name,
            offset=offset,
            limit=limit,
        ).pack()
    )]
    if button not in base_keyboard.inline_keyboard:
        base_keyboard.inline_keyboard.append(button)
    return base_keyboard
