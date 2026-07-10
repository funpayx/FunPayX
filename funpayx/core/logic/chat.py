from aiogram import Bot
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.engine import Session
from core.logic.repo.chat_repo import ChatRepo
from utils.bot_manager import BotManager


class ChatLogic:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bot: Bot = BotManager.get()
        self.repo = ChatRepo(db)

    async def message_all_users(self, **kwargs):
        users = await self.repo.get_user_list()
        for user in users:
            try:
                await self.bot.send_message(user.user_id, **kwargs)
            except Exception as e:
                logging.info(f'При отправке сообщения произошла ошибка: {e}')