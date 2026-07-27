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

    async def change_lot_name(self, lot_id, new_name_ru, new_name_en):
        await self.fpx.account.editor.change_lot_short_desc(lot_id, new_name_ru, new_name_en)

    async def change_lot_desc(self, lot_id, new_desc_ru, new_desc_en):
        await self.fpx.account.editor.change_lot_desc(lot_id, new_desc_ru, new_desc_en)

    async def change_lot_amount(self, lot_id, new_amount):
        await self.fpx.account.editor.change_lot_amount(lot_id, new_amount)

    async def get_lot_secrets(self, lot_id):
        return await self.fpx.account.lot.get_lot_secrets(lot_id)

    async def update_lot_secrets(self, lot_id, raw_secrets, rewrite):
        secrets = raw_secrets.split('\n')
        await self.fpx.account.editor.set_lot_secrets(lot_id, secrets, rewrite)

    async def delete_lot(self, lot_id):
        await self.fpx.account.editor.delete_lot(lot_id)