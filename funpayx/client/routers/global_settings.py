from aiogram import Router, F, types

from client.keyboards.gsettings_menu import global_settings_builder
from utils.config_manager import config_manager
from core.logic.settings import Settings


router = Router()


@router.callback_query(F.data.startswith('settings:toggle:'))
async def global_settings_toggle(callback: types.CallbackQuery):
    option = callback.data.split(':')[-1]
    settings = Settings()
    await settings.toggle_global_settings(option)
    await callback.message.edit_text(
        text='Выберите нужную опцию',
        reply_markup=global_settings_builder(config_manager.global_settings)
    )
    await callback.answer()

@router.callback_query(F.data == 'settings')
async def global_settings(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text='Выберите нужную опцию',
        reply_markup=global_settings_builder(config_manager.global_settings)
    )
    await callback.answer()