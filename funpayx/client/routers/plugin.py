import zipfile
import io
from pathlib import Path
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from client.keyboards.main_menu import back_to_main_menu
from utils.bot_manager import BotManager
from core.logic.plugins import PluginManager
from client.keyboards.plugins_menu import plugin_marketplace_menu, selected_plugin_menu, plugin_remover_menu


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

@router.callback_query(F.data.startswith('plugins:page:'))
async def get_plugins_market(callback: types.CallbackQuery):
    plugin_manager = PluginManager()
    page = callback.data.split(':')[-1]
    market = plugin_manager.get_marketplace()
    await callback.message.edit_text(f'Выбери нужный плагин', reply_markup=plugin_marketplace_menu(market, page))
    await callback.answer()

@router.callback_query(F.data.startswith('plugin:sel:'))
async def select_plugin(callback: types.CallbackQuery):
    plugin_id = callback.data.split(':')[-1]
    plugin_manager = PluginManager()
    plugin = plugin_manager.find_plugin_by_id(plugin_id)
    await callback.message.edit_text(
        text = f"""
<b>{plugin['title']}</b>

🆔 <b>ID:</b> <code>{plugin['id']}</code>
👤 <b>Автор:</b> <a href="https://github.com/{plugin['repo'].split('/')[0]}">{plugin['repo'].split('/')[0]}</a>
📦 <b>Репозиторий:</b> <a href="https://github.com/{plugin['repo']}">{plugin['repo']}</a>
🔖 <b>Коммит:</b> <code>{plugin['commit'][:7]}</code>
✅ <b>Проверил:</b> {plugin['verified_by']}
            """,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=selected_plugin_menu(plugin)
    )

@router.callback_query(F.data.startswith('install:'))
async def install_plugin(callback: types.CallbackQuery):
    plugin_id = callback.data.split(':')[-1]
    plugin_manager = PluginManager()
    plugin = plugin_manager.find_plugin_by_id(plugin_id)
    await plugin_manager.install_from_marketplace(plugin)
    await callback.message.edit_text('Успешно установлено. Введи /restart чтобы активировать')

@router.callback_query(F.data == 'plugins:remover')
async def plugin_remover(callback: types.CallbackQuery):
    await callback.message.edit_text('Выбери плагин, который хочешь удалить', reply_markup=plugin_remover_menu())

@router.callback_query(F.data.startswith('plugin:del:'))
async def delete_plugin(callback: types.CallbackQuery):
    plugin_id = callback.data.split(':')[-1]
    plugin_manager = PluginManager()
    response = plugin_manager.delete_plugin(plugin_id)
    await callback.message.edit_text(response, reply_markup=back_to_main_menu())