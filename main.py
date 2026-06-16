import asyncio
import logging
from aiogram import Bot, Dispatcher, Router

from config import BOT_TOKEN
from client.middlewares.db_session import DbSessionMiddleware
from core.database.engine import Session, init_db

from client.routers.error import router as error_router
from client.routers.common import router as common_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()
@router.error()
async def error_handler(event: types.ErrorEvent):
    logging.error(f"ОШИБКА: {event.exception}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await init_db()

    dp.update.middleware.register(DbSessionMiddleware(Session))

    dp.include_router(error_router)
    dp.include_router(common_router)

    logging.info('Бот запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.info('Запускаем бота')
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')