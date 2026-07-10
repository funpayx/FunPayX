from fpx import FunPayTools
from aiogram import Bot
import logging
import asyncio

from config import GKEY, GSEAL
from fpworker.routers.message import router as msg_router
from fpworker.routers.order import router as order_router
from fpworker.routers.review import router as review_router
from utils.funpay_manager import FunPayManager
from utils.plugin_manager import load_plugins
from core.logic.events import EventLogic


async def funpaymain():
    FunPayManager.init(GKEY, GSEAL)
    fp = FunPayManager.get()
    from fpworker.di_list import get_db
    from core.logic.chat import ChatLogic

    @fp.router.on_startup()
    async def answer_for_start():
        logging.info('Слушатель funpay запущен')
    fp.router.include_router(msg_router)
    fp.router.include_router(order_router)
    fp.router.include_router(review_router)
    load_plugins(fp)
    try:
        event = EventLogic()
        asyncio.create_task(event.back_task_manager())
        await fp.runner.start_polling(1, is_background=False)
    except asyncio.CancelledError:
        logging.info('Слушатель получил сигнал завершения')
        await fp.shutdown()
        raise