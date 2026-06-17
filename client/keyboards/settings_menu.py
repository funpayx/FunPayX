from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.config_manager import config_manager


def _status_icon(enabled: bool) -> str:
    return "✅" if enabled else "❌"

def settings_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    icon = _status_icon(config_manager.new_message_notifications)
    builder.row(
        InlineKeyboardButton(
            text=f"Уведомлять о новых сообщениях: {icon}",
            callback_data="settings:toggle_notifications",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Чёрный список отправителей",
            callback_data="blacklist:page:0",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="← Назад",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()

ITEMS_PER_PAGE = 10


def _paginate_blacklist(
    blacklist: list[str],
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    total_pages = max(1, (len(blacklist) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_items = blacklist[start:end]
    if not page_items:
        builder.row(
            InlineKeyboardButton(
                text="Список пуст",
                callback_data="blacklist:nop",
            )
        )
    else:
        for user_id in page_items:
            builder.row(
                InlineKeyboardButton(
                    text=f"❌ {user_id}",
                    callback_data=f"blacklist:remove:{user_id}",
                )
            )
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"blacklist:page:{page - 1}",
                )
            )
        nav_buttons.append(
            InlineKeyboardButton(
                text=f"{page + 1}/{total_pages}",
                callback_data="blacklist:nop",
            )
        )
        if page < total_pages - 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="➡️ Вперёд",
                    callback_data=f"blacklist:page:{page + 1}",
                )
            )
        builder.row(*nav_buttons)

    # Кнопка добавления пользователя
    builder.row(
        InlineKeyboardButton(
            text="➕ Добавить в ЧС",
            callback_data="blacklist:add_prompt",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="← Настройки",
            callback_data="settings_menu",
        )
    )
    return builder.as_markup()

__all__ = (
    "settings_menu",
    "_paginate_blacklist",
    "ITEMS_PER_PAGE",
)