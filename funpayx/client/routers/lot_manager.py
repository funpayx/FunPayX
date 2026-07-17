from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.logic.events import EventLogic
from client.keyboards.lot_manager_menu import create_lot_paginator, lot_info_manager
from client.keyboards.main_menu import back_to_main_menu, main_menu_kb


class PriceChange(StatesGroup):
    price_waiting = State()

router = Router()

@router.callback_query(F.data.startswith('lot:page:'))
async def lot_manager_open(callback: types.CallbackQuery):
    page = callback.data.split(':')[-1]
    event = EventLogic()
    lots = await event.get_user_lots()
    await callback.message.edit_text('Выбери лот', reply_markup=create_lot_paginator(lots, page))
    await callback.answer()

@router.callback_query(F.data.startswith('lot:toggle:'))
async def toggle_lot(callback: types.CallbackQuery, db):
    lot_id = callback.data.split(':')[-1]
    action = callback.data.split(':')[-2]
    event = EventLogic()
    await event.toggle_lot(lot_id, action, db)
    await callback.answer('Успешно')

@router.callback_query(F.data.startswith(f'lot:price:'))
async def change_lot_price(callback: types.CallbackQuery, state: FSMContext):
    lot_id = callback.data.split(':')[-1]
    await state.update_data(lot_id=lot_id)
    await callback.message.edit_text('Введите новую сумму денег', reply_markup=back_to_main_menu())
    await callback.answer()
    await state.set_state(PriceChange.price_waiting)

@router.message(PriceChange.price_waiting)
async def change_lot_price_processing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lot_id = data.get('lot_id')
    new_price = message.text
    await state.clear()
    event = EventLogic()
    await event.change_lot_price(lot_id, new_price)
    await message.answer('Успешно изменено', reply_markup=main_menu_kb())

@router.callback_query(F.data.startswith('lot:'))
async def lot_info(callback: types.CallbackQuery):
    lot_id = callback.data.split(':')[-1]
    event = EventLogic()
    lot = await event.get_lot_info(lot_id)
    text = (f"""
📦 <b>Лот #{lot.id}</b>
    
🏷 <b>Название:</b> {lot.short_desc}
📝 <b>Описание:</b> {lot.description}
    
💰 <b>Цена:</b> <b>{lot.price} ₽</b>
""")
    await callback.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=lot_info_manager(lot_id)
    )