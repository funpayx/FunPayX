from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def message_kb(chat_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Ответить на сообщение",
            callback_data=f"message:answer:{chat_id}",
        )
    )
    return builder.as_markup()