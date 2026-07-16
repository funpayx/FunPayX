import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, Router

from config import BOT_TOKEN
from client.middlewares.db_session import DbSessionMiddleware
from core.database.engine import Session, init_db
from utils.bot_manager import BotManager, DpManager
from utils.config_manager import config_manager

from client.routers.error import router as error_router
from client.routers.common import router as common_router
from client.routers.settings import router as setting_router
from client.routers.events import router as event_router
from client.routers.global_settings import router as global_settings_router


router = Router()
@router.error()
async def error_handler(event: types.ErrorEvent):
    logging.error(f"ОШИБКА: {event.exception}")

async def botmain():
    BotManager.init(BOT_TOKEN)
    bot = BotManager.get()
    DpManager.init()
    dp = DpManager.get()
    await init_db()
    await config_manager.load_config()
    dp.update.middleware.register(DbSessionMiddleware(Session))

    dp.include_router(error_router)
    dp.include_routers(common_router, setting_router, event_router, global_settings_router)

    restarted_by = os.environ.pop('FPX_RESTARTED_BY', None)
    if restarted_by:
        try:
            await bot.send_message(restarted_by, '✅ Бот перезапущен. Пропиши /start')
        except Exception as e:
            logging.warning(f'Не удалось отправить сообщение о запуске: {e}')
    
    logging.info('Бот запущен')
    await dp.start_polling(bot)