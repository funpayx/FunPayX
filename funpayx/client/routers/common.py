import asyncio
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.logic.user import UserLogic
from client.keyboards.main_menu import main_menu_kb, plugin_menu
from utils.restarter import restart_process


router = Router()

class Auth(StatesGroup):
    waiting_password = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, db):
    user = UserLogic(db, message.from_user.id)
    if await user.is_authorized():
        return await message.answer('Добро пожаловать', reply_markup=main_menu_kb())
    await message.answer('Введи свой пароль')
    await state.set_state(Auth.waiting_password)

@router.message(Auth.waiting_password)
async def auth_processing(message: types.Message, state: FSMContext, db):
    user = UserLogic(db, message.from_user.id)
    if await user.auth(message.text):
        return await message.answer('Добро пожаловать', reply_markup=main_menu_kb())
    await state.clear()
    
@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: types.CallbackQuery, state: FSMContext, db):
    user = UserLogic(db, callback.from_user.id)
    if await user.is_authorized():
        return await callback.message.edit_text('Добро пожаловать', reply_markup=main_menu_kb())
    await callback.message.edit_text('Введи свой пароль')
    await state.set_state(Auth.waiting_password)

@router.callback_query(F.data == 'plugins')
async def handle_plugin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(f'Меню плагинов', reply_markup=plugin_menu())
    await callback.answer()

@router.message(Command('restart'))
async def restart_cmd(message: types.Message, db):
    user = UserLogic(db, message.from_user.id)
    if not await user.is_authorized():
        return await message.answer('Отказано в доступе!')
    await message.answer('♻️ Перезапускаюсь...')
    restart_process(message.from_user.id)
    await message.answer('Успешно перезапущено', reply_markup=main_menu_kb())