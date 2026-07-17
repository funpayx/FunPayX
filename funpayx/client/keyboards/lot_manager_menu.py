from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Protocol
from fpx.models.lots import LotInfo


def create_lot_paginator(
    lots: list[LotInfo],
    page: int = 0,
    per_page: int = 10,
) -> InlineKeyboardMarkup:
    total_pages = int(max(1, (len(lots) + per_page - 1) // per_page))
    page = max(0, min(int(page), total_pages - 1)) 
    start = page * per_page
    end = start + per_page
    page_lots = lots[start:end]
    builder = InlineKeyboardBuilder()
    for lot in page_lots:
        builder.row(
            InlineKeyboardButton(
                text=lot.name,
                callback_data=f"lot:{lot.id}",
            )
        )
    nav_row = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"lot:page:{page - 1}",
            )
        )
    nav_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="none",
        )
    )
    if page < total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"lot:page:{page + 1}",
            )
        )
    builder.row(*nav_row)
    builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='main_menu',
            style='danger'
        )
    )
    return builder.as_markup()

def lot_info_manager(lot_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Сменить цену',
            callback_data=f'lot:price:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Скрыть лот',
            callback_data=f'lot:toggle:off:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Показать лот',
            callback_data=f'lot:toggle:on:{lot_id}'
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