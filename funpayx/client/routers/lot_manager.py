from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.logic.events import EventLogic
from client.keyboards.lot_manager_menu import create_lot_paginator, lot_info_manager
from client.keyboards.main_menu import back_to_main_menu, main_menu_kb


class PriceChange(StatesGroup):
    price_waiting = State()

class NameChange(StatesGroup):
    ru_name_waiting = State()
    en_name_waiting = State()
    confirm_waiting = State()

class DescChange(StatesGroup):
    ru_desc_waiting = State()
    en_desc_waiting = State()
    confirm_waiting = State()

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

@router.callback_query(F.data.startswith('lot:name:'))
async def lot_name(callback: types.CallbackQuery, state: FSMContext):
    lot_id = callback.data.split(':')[-1]
    await state.update_data(lot_id=lot_id)
    await callback.message.edit_text(f'Введите новое название лота на русском', reply_markup=back_to_main_menu())
    await state.set_state(NameChange.ru_name_waiting)
    await callback.answer()

@router.callback_query(F.data.startswith('lot:desc:'))
async def lot_name(callback: types.CallbackQuery, state: FSMContext):
    lot_id = callback.data.split(':')[-1]
    await state.update_data(lot_id=lot_id)
    await callback.message.edit_text(f'Введите новое описание лота на русском', reply_markup=back_to_main_menu())
    await state.set_state(DescChange.ru_desc_waiting)
    await callback.answer()

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

@router.message(NameChange.ru_name_waiting)
async def ru_name_saving(message: types.Message, state: FSMContext):
    name_ru = message.text
    await state.update_data(name_ru=name_ru)
    await message.answer(
        f'Записано. Новое название на русском:\n{name_ru}.\n Теперь введите название на английском',
        reply_markup=back_to_main_menu()
    )
    await state.set_state(NameChange.en_name_waiting)

@router.message(NameChange.en_name_waiting)
async def en_name_saving(message: types.Message, state: FSMContext):
    name_en = message.text
    await state.update_data(name_en=name_en)
    await message.answer(
        f'Записано. Новое название на английском:\n{name_en}.\n Вы уверены, что записали всё верно?\nСкопируйте, и введите в чат `Да, согласен` если всё нормально, и `Нет, заново` если что-то не так.',
        parse_mode='markdown',
        reply_markup=back_to_main_menu()
    )
    await state.set_state(NameChange.confirm_waiting)

@router.message(NameChange.confirm_waiting)
async def lot_name_change_confirming(message: types.Message, state: FSMContext):
    confirm_text = message.text
    data = await state.get_data()
    lot_id = data.get('lot_id')
    name_ru = data.get('name_ru')
    name_en = data.get('name_en')
    if confirm_text == 'Да, согласен':
        event = EventLogic()
        await event.change_lot_name(lot_id, name_ru, name_en)
        await state.clear()
        await message.answer('Успешно изменено!', reply_markup=back_to_main_menu())
    else:
        await state.clear()
        await state.update_data(lot_id=lot_id)
        await message.answer('Введите новое название лота на русском', reply_markup=back_to_main_menu())
        await state.set_state(NameChange.ru_name_waiting)


@router.message(DescChange.ru_desc_waiting)
async def ru_name_saving(message: types.Message, state: FSMContext):
    name_ru = message.text
    await state.update_data(name_ru=name_ru)
    await message.answer(
        f'Записано. Новое описание на русском:\n{name_ru}.\n Теперь введите описание на английском',
        reply_markup=back_to_main_menu()
    )
    await state.set_state(DescChange.en_desc_waiting)

@router.message(DescChange.en_desc_waiting)
async def en_name_saving(message: types.Message, state: FSMContext):
    name_en = message.text
    await state.update_data(name_en=name_en)
    await message.answer(
        f'Записано. Новое описание на английском:\n{name_en}.\n Вы уверены, что записали всё верно?\nСкопируйте, и введите в чат `Да, согласен` если всё нормально, и `Нет, заново` если что-то не так.',
        parse_mode='markdown',
        reply_markup=back_to_main_menu()
    )
    await state.set_state(DescChange.confirm_waiting)

@router.message(DescChange.confirm_waiting)
async def lot_name_change_confirming(message: types.Message, state: FSMContext):
    confirm_text = message.text
    data = await state.get_data()
    lot_id = data.get('lot_id')
    name_ru = data.get('name_ru')
    name_en = data.get('name_en')
    if confirm_text == 'Да, согласен':
        event = EventLogic()
        await event.change_lot_desc(lot_id, name_ru, name_en)
        await state.clear()
        await message.answer('Успешно изменено!', reply_markup=back_to_main_menu())
    else:
        await state.clear()
        await state.update_data(lot_id=lot_id)
        await message.answer('Введите новое описание лота на русском', reply_markup=back_to_main_menu())
        await state.set_state(DescChange.ru_desc_waiting)