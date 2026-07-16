import zipfile
import io
from pathlib import Path
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from client.keyboards.main_menu import back_to_main_menu
from utils.bot_manager import BotManager


class PluginState(StatesGroup):
    waiting_archive = State()

router = Router()

PLUGINS_DIR = Path('plugins')

@router.callback_query(F.data == 'plugins:add')
async def add_plugin_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Отправьте zip архив с плагином, бот автоматически его распакует', 
        reply_markup=back_to_main_menu()
    )
    await state.set_state(PluginState.waiting_archive)

@router.message(PluginState.waiting_archive)
async def plugin_archive_adding(message: types.Message):
    doc = message.document
    if not doc.file_name.endswith('.zip'):
        return await message.answer('⚠️ Пришли плагин архивом .zip (папку целиком - просто запакуй перед отправкой).')
    bot = BotManager.get()
    file = await bot.get_file(doc.file_id)
    file_bytes = await bot.download_file(file.file_path)
    try:
        with zipfile.ZipFile(file_bytes) as zf:
            for member in zf.namelist():
                target = (PLUGINS_DIR / member).resolve()
                if not str(target).startswith(str(PLUGINS_DIR.resolve())):
                    return await message.answer('⚠️ Архив содержит подозрительные пути, отклонено.')
            zf.extractall(PLUGINS_DIR)
    except zipfile.BadZipFile:
        return await message.answer('⚠️ Файл повреждён или это не zip.')
    await message.answer('✅ Плагин установлен. Перезапусти бота командой /restart, чтобы он подгрузился.')