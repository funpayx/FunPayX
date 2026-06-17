from aiogram import F, types, Router

from client.keyboards.settings_menu import settings_menu
from core.logic.settings import Settings


router = Router()

@router.callback_query(F.data == 'settings_menu')
async def open_settings(callback: types.CallbackQuery):
    return await callback.message.edit_text('Выбери опцию:', reply_markup=settings_menu())

@router.callback_query(F.data == 'settings:toggle_notifications')
async def toggle_notify(callback: types.CallbackQuery):
    settings = Settings()
    await settings.toggle_notifications()
    return await callback.message.edit_text('Выбери опцию', reply_markup=settings_menu())