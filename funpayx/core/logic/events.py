import asyncio
from fpx import FunPayTools, types

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

    async def get_user_lots(self):
        profile = await self.fpx.account.profile.profile()
        lots = profile.lots
        return lots

    async def get_lot_info(self, lot_id):
        return await self.fpx.account.lot.get_lot_info(lot_id)

    async def toggle_lot(self, lot_id, action, db):
        if action == 'on':
            if config_manager.find_hidden_lot(lot_id):
                await self.fpx.account.editor.toggle_on_lot(lot_id)
                config_manager.hidden_lots.remove(lot_id)
        elif action == 'off':
            if not config_manager.find_hidden_lot(lot_id):
                await self.fpx.account.editor.toggle_off_lot(lot_id)
                config_manager.hidden_lots.append(lot_id)
        await config_manager.update_config()

    async def change_lot_price(self, lot_id, new_price):
        await self.fpx.account.editor.change_lot_price(lot_id, new_price)