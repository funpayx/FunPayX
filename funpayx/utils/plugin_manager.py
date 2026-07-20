import importlib.util
import sys
import types
import json
from pathlib import Path
from aiogram import Router as AioRouter
from aiogram import F
from fpx import Router as FpxRouter
from .bot_manager import DpManager, BotManager
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def plugin_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Настройки',
            callback_data=f'plugin:settings:{id}',
            style='primary'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Команды',
            callback_data=f'plugin:commands:1',
            style='primary'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='plugins',
            style='danger'
        )
    )
    return builder.as_markup()

plugin_data = {
    "routers": [
        "main.router",
        "client.router"
    ],
    "manifest": {
        "title": "TemplatePlugin",
        "description": "Шаблон оформления плагина, заполни plugin.json",
        "version": "1.0.0",
        "credits": [
            "@sanyalca"
        ],
        "custom_menu": True
    },
    "id": 0
}

main_py_code = ('''
from fpx import Router


router = Router()

# ты можешь продолжить создавать роутеры в других файлах, или оставить только в этом
''')

client_py_code = ('''
import os
import json
from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, 'plugin.json')

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

id = config['id']
manifest = config['manifest']

router = Router()

def plugin_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Настройки',
            callback_data=f'plugin:settings:{id}',
            style='primary'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Команды',
            callback_data=f'plugin:commands:{id}',
            style='primary'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='plugins',
            style='danger'
        )
    )
    return builder.as_markup()

def back_to_plugin() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'plugin_{id}',
            style='danger'
        )
    )
    return builder.as_markup()

credits_str = ", ".join(manifest.get("credits", []))
@router.callback_query(F.data == f'plugin_{id}')
async def plugin_start_handler(callback):
    await callback.message.edit_text(
        f'Название: {manifest['title']}\\n'
        f'Описание: {manifest['description']}\\n'
        f'Версия: v{manifest['version']}\\n'
        f'Контакты: {credits_str}',
        reply_markup=plugin_menu()
    )

@router.callback_query(F.data == f'plugin:settings:{id}')
async def plugin_settings(callback):
    await callback.message.edit_text(
        'Раздел настроек плагина. Если требуется, можно заполнить или удалить. По дефолту текст на 60 строке',
        reply_markup=back_to_plugin()
    )

@router.callback_query(F.data == f'plugin:commands:{id}')
async def dynamic_handler(callback):
    await callback.message.edit_text(
        'Раздел списка команд плагина. Если требуется, можно заполнить или удалить. По дефолту текст на 66 строке',
        reply_markup=back_to_plugin()
    )
'''
)

plugin_callback_list = []

router = AioRouter()

def load_router(router, manifest, id):
    def back_to_plugin() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'plugin_{id}',
                style='danger'
            )
        )
        return builder.as_markup()
    credits_str = ", ".join(manifest.get("credits", []))
    plugin_callback_list.append({'id': id, 'title': manifest['title']})
    async def dynamic_handler(callback):
        await callback.message.edit_text(
            f'Название: {manifest['title']}\n'
            f'Описание: {manifest['description']}\n'
            f'Версия: v{manifest['version']}\n'
            f'Контакты: {credits_str}',
            reply_markup=back_to_plugin()
        )
    if not manifest['custom_menu']:
        router.callback_query.register(dynamic_handler, F.data == f'plugin_{id}')

def ensure_package(name: str, path: str):
    if name not in sys.modules:
        pkg = types.ModuleType(name)
        pkg.__path__ = [path]
        sys.modules[name] = pkg

plugins_dir = Path('plugins')

def load_plugins(fp):
    plugins_dir.mkdir(parents=True, exist_ok=True)
    if plugins_dir.exists():
        dp = DpManager.get()
        plugin_id = 1
        for p_fol in plugins_dir.iterdir():
            if p_fol.is_dir():
                ensure_package('plugins', str(plugins_dir))
                ensure_package(f'plugins.{p_fol.name}', str(p_fol))
                main_file = p_fol / 'main.py'
                if not main_file.exists():
                    with open(main_file, "w", encoding="utf-8") as f:
                        f.write(main_py_code)
                client_file = p_fol / 'client.py'
                if not client_file.exists():
                    with open(client_file, "w", encoding="utf-8") as f:
                        f.write(client_py_code)
                config_file = p_fol / 'plugin.json'
                if not config_file.exists():
                    with open(config_file, "w", encoding="utf-8") as f:
                        json.dump(plugin_data, f, ensure_ascii=False, indent=2)
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                config['id'] = plugin_id
                with open(config_file, "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                routers_paths = config.get('routers', [])
                if isinstance(routers_paths, str):
                    routers_paths = [routers_paths]
                for r_path in routers_paths:
                    *file_parts, router_var_name = r_path.split('.')
                    file_rel_path = Path(*file_parts).with_suffix('.py')
                    router_file = p_fol / file_rel_path
                    if router_file.exists():
                        sub_module_name = '.'.join(file_parts)
                        module_name = f'plugins.{p_fol.name}.{sub_module_name}'
                        spec = importlib.util.spec_from_file_location(module_name, router_file)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                        plugin_router = getattr(module, router_var_name)
                        if isinstance(plugin_router, FpxRouter):
                            fp.router.include_router(plugin_router)
                        elif isinstance(plugin_router, AioRouter):
                            dp.include_router(plugin_router)
                manifest = config.get('manifest')
                load_router(router, manifest, plugin_id)
                plugin_id += 1
        dp.include_router(router)