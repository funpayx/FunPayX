from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.plugin_manager import plugin_callback_list


def plugin_marketplace_menu(marketplace_data: list[dict], page: int = 0) -> InlineKeyboardMarkup:
    ITEMS_PER_PAGE = 5 
    builder = InlineKeyboardBuilder()
    start = int(page * ITEMS_PER_PAGE)
    end = start + ITEMS_PER_PAGE
    page_items = marketplace_data[start:end]
    for item in page_items:
        builder.row(
            InlineKeyboardButton(
                text=item['title'],
                callback_data=f"plugin:sel:{item['id']}"
            )
        )
    total_pages = (len(marketplace_data) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                InlineKeyboardButton(text="⬅️ Назад", callback_data=f"plugins:page:{page - 1}")
            )
        nav_buttons.append(
            InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="none")
        )
        if page < total_pages - 1:
            nav_buttons.append(
                InlineKeyboardButton(text="▶️ Вперёд", callback_data=f"plugins:page:{page + 1}")
            )
        builder.row(*nav_buttons)
    builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data=f"main_menu",
            style='danger'
        )
    )
    return builder.as_markup()

def selected_plugin_menu(plugin):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Установить',
            callback_data=f'install:{plugin['id']}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data=f"main_menu",
            style='danger'
        )
    )
    return builder.as_markup()

def plugin_remover_menu():
    builder = InlineKeyboardBuilder()
    for plugin in plugin_callback_list:
        builder.row(
            InlineKeyboardButton(
                text=plugin['title'],
                callback_data=f'plugin:del:{plugin['id']}'
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data=f"main_menu",
            style='danger'
        )
    )
    return builder.as_markup()