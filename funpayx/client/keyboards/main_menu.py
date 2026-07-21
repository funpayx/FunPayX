from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.plugin_manager import plugin_callback_list


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
    builder.row(
        InlineKeyboardButton(
            text='Плагины',
            callback_data='plugins'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Управление лотами',
            callback_data='lot:page:0'
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

def plugin_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for plugin in plugin_callback_list:
        builder.row(
            InlineKeyboardButton(
                text=plugin['title'],
                callback_data=f'plugin_{plugin['id']}'
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='Маркетплейс',
            callback_data='plugins:page:0',
            style='success'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Добавить плагин',
            callback_data='plugins:add',
            style='primary'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Удаление плагинов',
            callback_data='plugins:remover',
            style='primary'
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
