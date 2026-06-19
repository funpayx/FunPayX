import asyncio
import logging
from aiogram import Bot, Dispatcher, Router

from config import BOT_TOKEN
from client.middlewares.db_session import DbSessionMiddleware
from core.database.engine import Session, init_db
from utils.bot_manager import BotManager
from utils.config_manager import config_manager

from client.routers.error import router as error_router
from client.routers.common import router as common_router
from client.routers.settings import router as setting_router
from client.routers.events import router as event_router

router = Router()
@router.error()
async def error_handler(event: types.ErrorEvent):
    logging.error(f"ОШИБКА: {event.exception}")

async def botmain():
    BotManager.init(BOT_TOKEN)
    bot = BotManager.get()
    dp = Dispatcher()
    await init_db()
    await config_manager.load_config()
    dp.update.middleware.register(DbSessionMiddleware(Session))

    dp.include_router(error_router)
    dp.include_routers(common_router, setting_router, event_router)
    
    logging.info('Бот запущен')
    await dp.start_polling(bot)