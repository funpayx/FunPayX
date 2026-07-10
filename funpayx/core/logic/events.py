import asyncio
from fpx import FunPayTools

from utils.funpay_manager import FunPayManager
from utils.exceptions import BotError
from utils.config_manager import config_manager


class EventLogic:
    def __init__(self):
        self.fpx: FunPayTools = FunPayManager.get()

    async def send_message(self, chat_id, text):
        try:
            return await self.fpx.account.chat.send_message(chat_id, text)
        except Exception as e:
            raise BotError(e)

    async def refund_order(self, order_id):
        await self.fpx.account.order.refund_order(order_id)

    async def back_task_manager(self):
        await asyncio.sleep(10)
        while True:
            if config_manager.global_settings['auto_raise']:
                await self.fpx.account.lot.raise_lots()
            await asyncio.sleep(3600)