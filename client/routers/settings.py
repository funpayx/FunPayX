from aiogram import F, types, Router

from client.keyboards.settings_menu import settings_menu


router = Router()

@router.callback_query(F.data == 'settings_menu')
async def open_settings(callback: types.CallbackQuery):
    return await callback.message.edit_text('Выбери опцию:', reply_markup=settings_menu())