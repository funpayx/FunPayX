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
            text='Изменить название',
            callback_data=f'lot:name:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Изменить описание',
            callback_data=f'lot:desc:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Сменить цену',
            callback_data=f'lot:price:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Менеджер секретов (автовыдачи)',
            callback_data=f'lot:secrets:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Обновить наличие лота',
            callback_data=f'lot:amount:{lot_id}'
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
            text='Удалить лот',
            callback_data=f'lot:delete:{lot_id}'
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

def back_to_lot(lot_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Назад к лоту',
            callback_data=f'lot:{lot_id}',
            style='danger'
        )
    )
    return builder.as_markup()

def change_secrets_kb(lot_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить новый товар к уже существующему',
            callback_data=f'lot:sec:add:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Перезаписать секреты с нуля',
            callback_data=f'lot:sec:rew:{lot_id}'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад к лоту',
            callback_data=f'lot:{lot_id}',
            style='danger'
        )
    )
    return builder.as_markup()

def lot_delete_confirmer(lot_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Согласен',
            callback_data=f'lot:delete:ok{lot_id}',
            style='success'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад к лоту',
            callback_data=f'lot:{lot_id}',
            style='danger'
        )
    )
    return builder.as_markup()