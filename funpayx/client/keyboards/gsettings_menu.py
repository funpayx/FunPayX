from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_status(setting):
    return '🟢' if setting else '🔴'

def global_settings_builder(global_settings) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'{get_status(global_settings['auto_raise'])} Автоподнятие',
            callback_data='settings:toggle:raise'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'{get_status(global_settings['auto_delivery'])} Автовыдача',
            callback_data='settings:toggle:delivery'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'{get_status(global_settings['auto_answer'])} Автоответчик',
            callback_data='settings:toggle:answer'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='main_menu',
            style='danger'
        )
    )
    return builder.as_markup()