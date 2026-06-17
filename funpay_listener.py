from fpx import FunPayTools, Message, Dependency
from aiogram import Bot
import logging
import asyncio

from config import GKEY
from fpworker.routers.message import router as msg_router
from core.logic.events import EventLogic
from utils.funpay_manager import FunPayManager


async def funpaymain():
    FunPayManager.init(GKEY)
    fp = FunPayManager.get()
    from fpworker.di_list import get_db
    from core.logic.chat import ChatLogic

    @fp.router.on_startup()
    async def answer_for_start():
        logging.info('Слушатель funpay запущен')
    fp.router.include_router(msg_router)
    try:
        await fp.runner.start_polling(1, is_background=False)
    except asyncio.CancelledError:
        logging.info('Слушатель получил сигнал завершения')
        await fp.shutdown()
        raise