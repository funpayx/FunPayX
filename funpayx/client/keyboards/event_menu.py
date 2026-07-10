from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def message_kb(chat_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Ответить",
            callback_data=f"message:answer:{chat_id}",
        ),
        InlineKeyboardButton(
            text='В чат',
            url=f'https://funpay.com/chat/?node={chat_id}'
        )
    )
    return builder.as_markup()

def get_order_keyboard(order_id, chat_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💸 Вернуть деньги", callback_data=f"order:ref:{order_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🌐 Открыть страницу заказа", url=f"https://funpay.com/orders/{order_id}/")
    )
    builder.row(
        InlineKeyboardButton(text="📩 Ответить", callback_data=f"order:answer:{chat_id}")
    )
    return builder.as_markup()