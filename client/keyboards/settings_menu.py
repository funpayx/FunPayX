from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.config_manager import config_manager


def _status_icon(enabled: bool) -> str:
    return "✅" if enabled else "❌"

def settings_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"Уведомлять о новых сообщениях: {_status_icon(config_manager.new_message_notifications)}",
            callback_data="notify:toggle_messages",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Уведомлять о новых заказах: {_status_icon(config_manager.new_order_notifications)}",
            callback_data="notify:toggle_new_orders",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Уведомлять о подтвержденных заказах: {_status_icon(config_manager.closed_order_notifications)}",
            callback_data="notify:toggle_closed_orders",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Уведомлять о возвратах: {_status_icon(config_manager.refunded_order_notifications)}",
            callback_data="notify:toggle_refunded_orders",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Уведомлять о новых отзывах: {_status_icon(config_manager.new_review_notifications)}",
            callback_data="notify:toggle_new_reviews",
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
    start = int(page * ITEMS_PER_PAGE)
    end = int(start + ITEMS_PER_PAGE)
    page_items = blacklist[start:end]
    if not page_items:
        builder.row(
            InlineKeyboardButton(
                text="Список пуст",
                callback_data="blacklist:nop",
            )
        )
    else:
        for user_name in page_items:
            builder.row(
                InlineKeyboardButton(
                    text=f"❌ {user_name}",
                    callback_data=f"blacklist:rm:{user_name}:{page}",
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
    builder.row(
        InlineKeyboardButton(
            text="➕ Добавить в ЧС",
            callback_data=f"blacklist:add_prompt:{page}",
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