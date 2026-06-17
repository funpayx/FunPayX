from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import BaseConfig
from fpworker.di_list import get_db


class ConfigManager:
    def __init__(self):
        self.new_message_notifications: bool = True
        self.blacklist_buyers: list = []
    
    async def load_config(self):
        '''Загрузка конфига в память при старте'''
        db: AsyncSession = await get_db()
        result = await db.execute(select(BaseConfig))
        config = result.scalars().all()
        if config:
            self.new_message_notifications = config.new_message_notifications
            self.blacklist_buyers = config.blacklist_buyers

    async def update_config(self):
        '''Обновление конфига в бд и кеш'''
        db: AsyncSession = await get_db()
        result = await db.execute(select(BaseConfig))
        config = result.scalars().first()
        if config is None:
            config = BaseConfig(
                new_message_notifications=self.new_message_notifications,
                blacklist_buyers=self.blacklist_buyers
            )
            db.add(config)
        else:
            config.new_message_notifications = self.new_message_notifications
            config.blacklist_buyers = self.blacklist_buyers
        await db.commit()

config_manager = ConfigManager()