from fpx import FunPayTools
from aiogram import Bot
import logging
import asyncio

from config import GKEY
from fpworker.routers.message import router as msg_router
from fpworker.routers.order import router as order_router
from fpworker.routers.review import router as review_router
from utils.funpay_manager import FunPayManager
from utils.plugin_manager import load_plugins
from core.logic.events import EventLogic
from config import FUNPAY_PROXY


async def funpaymain():
    FunPayManager.init(GKEY, FUNPAY_PROXY)
    fp = FunPayManager.get()
    from fpworker.di_list import get_db
    from core.logic.chat import ChatLogic

    @fp.router.on_startup()
    async def answer_for_start():
        logging.info('Слушатель funpay запущен')
    load_plugins(fp)
    fp.router.include_router(msg_router)
    fp.router.include_router(order_router)
    fp.router.include_router(review_router)
    try:
        event = EventLogic()
        asyncio.create_task(event.back_task_manager())
        await fp.runner.start_polling(1, is_background=False)
    except asyncio.CancelledError:
        logging.info('Слушатель получил сигнал завершения')
        await fp.shutdown()
        raise