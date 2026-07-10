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
            text="← Меню",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()

def set_meeting() -> InlineKeyboardMarkup:
    cooldown = config_manager.welcome_msg.get('time')
    cooldown = int(cooldown)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'Приветствовать пользователей: {_status_icon(config_manager.welcome_msg['enabled'])}', 
            callback_data='meeting:toggle:meet_user'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'Игнорировать системные сообщения: {_status_icon(config_manager.welcome_msg['ignore_system'])}',
            callback_data='meeting:toggle:system'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'Только в новых диалогах: {_status_icon(config_manager.welcome_msg['only_new'])}',
            callback_data='meeting:toggle:only_new'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Изменить приветственное сообщение',
            callback_data='meeting:change:message'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'{"".join([f"{cooldown // 24}дн. " if cooldown >= 24 else "", f"{cooldown % 24}час." if cooldown % 24 != 0 else ""]).strip()}',
            callback_data='meeting:change:cooldown'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='main_menu'
        )
    )
    return builder.as_markup()

def _check_command(enabled):
    return "✅" if enabled else "❌"

def paginate_commands(
    command_list: list[dict],
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    total_pages = max(1, (len(command_list) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    start = int(page * ITEMS_PER_PAGE)
    end = int(start + ITEMS_PER_PAGE)
    page_items = command_list[start:end]
    if not page_items:
        builder.row(
            InlineKeyboardButton(
                text="Список пуст",
                callback_data="command:nop",
            )
        )
    else:
        for answ in page_items:
            builder.row(
                InlineKeyboardButton(
                    text=f"{_check_command(answ['enabled'])} {answ['command']}",
                    callback_data=f"command:edit:{answ['command']}",
                )
            )
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"command:page:{page - 1}",
                )
            )
        nav_buttons.append(
            InlineKeyboardButton(
                text=f"{page + 1}/{total_pages}",
                callback_data="command:nop",
            )
        )
        if page < total_pages - 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="➡️ Вперёд",
                    callback_data=f"command:page:{page + 1}",
                )
            )
        builder.row(*nav_buttons)
    builder.row(
        InlineKeyboardButton(
            text="➕ Добавить команду",
            callback_data=f"command:new:{page}",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="← Меню",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()

def command_settings_kb(data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="✏️ Редактировать сообщение",
            callback_data=f"command:set:msg:{data['command']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"📢 Уведомлять в Telegram: {_status_icon(data.get('ping_user', False))}",
            callback_data=f"command:toggle:notify:{data['command']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📝 Редактировать команду",
            callback_data=f"command:set:cmd:{data['command']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"▶️ Запущено: {_status_icon(data.get('enabled', False))}",
            callback_data=f"command:toggle:enabled:{data['command']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Удалить",
            callback_data=f"command:delete:{data['command']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="← Назад",
            callback_data=f"command:page:0"
        )
    )
    
    return builder.as_markup()