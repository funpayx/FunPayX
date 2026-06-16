from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.logic.user import UserLogic

router = Router()

class Auth(StatesGroup):
    waiting_password = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, db):
    user = UserLogic(db, message.from_user.id)
    if await user.is_authorized():
        return await message.answer('Добро пожаловать')
    await message.answer('Введи свой пароль')
    await state.set_state(Auth.waiting_password)

@router.message(Auth.waiting_password)
async def auth_processing(message: types.Message, state: FSMContext, db):
    user = UserLogic(db, message.from_user.id)
    if await user.auth(message.text):
        return await message.answer('Добро пожаловать')
    
@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: types.CallbackQuery, state: FSMContext, db):
    user = UserLogic(db, callback.from_user.id)
    if await user.is_authorized():
        return await callback.message.edit_text('Добро пожаловать')
    await callback.message.edit_text('Введи свой пароль')
    await state.set_state(Auth.waiting_password)