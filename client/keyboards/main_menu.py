from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Настройки уведомлений",
            callback_data="settings_menu",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📃 Чёрный список",
            callback_data="blacklist:page:0",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="👋 Приветственное сообщение",
            callback_data="meeting:set",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='🤖 Управление командами',
            callback_data='command:page:0'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='⚙️ Глобальные переключатели',
            callback_data='settings'
        )
    )
    return builder.as_markup()

def back_to_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='main_menu',
            style='danger'
        )
    )
    return builder.as_markup()