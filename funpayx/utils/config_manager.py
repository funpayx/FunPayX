from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.engine import Session
from core.database.models import BaseConfig


class ConfigManager:
    def __init__(self):
        self.new_message_notifications: bool = True
        self.new_order_notifications: bool = True
        self.closed_order_notifications: bool = True
        self.refunded_order_notifications: bool = True
        self.new_review_notifications: bool = True
        self.welcome_msg: dict = {
            'time': 24,
            'enabled': False,
            'ignore_system': True,
            'only_new': False,
            'message': 'Привет, {sender}!'
        }
        self.accept_order_answer: str = None
        self.review_answer: dict = None
        self.blacklist_buyers: list = []
        self.auto_issue: dict = None
        self.auto_answer: list[dict] = [
            {
                'command': '!start',
                'enabled': False,
                'ping_user': True,
                'message': 'Привет! Я позвал продавца'
            },
        ]
        self.global_settings: dict = {
            'auto_raise': False,
            'auto_delivery': False,
            'auto_answer': False
        }
        self.hidden_lots: list = []
    
    async def load_config(self):
        '''Загрузка конфига в память при старте'''
        async with Session() as db:
            result = await db.execute(select(BaseConfig))
            config = result.scalars().first()
            if config:
                self.new_message_notifications = config.new_message_notifications
                self.blacklist_buyers = config.blacklist_buyers
                self.new_order_notifications = config.new_order_notifications
                self.closed_order_notifications = config.closed_order_notifications
                self.new_review_notifications = config.new_review_notifications
                self.welcome_msg = config.welcome_msg
                self.accept_order_answer = config.accept_order_answer
                self.review_answer = config.review_answer
                self.auto_issue = config.auto_issue
                self.auto_answer = config.auto_answer
                self.global_settings = config.global_settings
                self.hidden_lots = config.hidden_lots

    async def update_config(self):
        '''Обновление конфига в бд и кеш'''
        async with Session() as db:
            result = await db.execute(select(BaseConfig))
            config = result.scalars().first()
            if config is None:
                config = BaseConfig(
                    new_message_notifications=self.new_message_notifications,
                    blacklist_buyers=self.blacklist_buyers,
                    new_order_notifications=self.new_order_notifications,
                    closed_order_notifications=self.closed_order_notifications,
                    new_review_notifications=self.new_review_notifications,
                    welcome_msg=self.welcome_msg,
                    accept_order_answer = self.accept_order_answer,
                    review_answer=self.review_answer,
                    auto_answer=self.auto_answer,
                    auto_issue=self.auto_issue,
                    global_settings=self.global_settings,
                    hidden_lots=self.hidden_lots
                )
                db.add(config)
            else:
                config.new_message_notifications = self.new_message_notifications
                config.blacklist_buyers = self.blacklist_buyers
                config.new_order_notifications=self.new_order_notifications
                config.closed_order_notifications=self.closed_order_notifications
                config.new_review_notifications=self.new_review_notifications
                config.welcome_msg=self.welcome_msg
                config.accept_order_answer = self.accept_order_answer
                config.review_answer=self.review_answer
                config.auto_answer=self.auto_answer
                config.auto_issue=self.auto_issue
                config.global_settings=self.global_settings
                config.hidden_lots=self.hidden_lots
            await db.commit()

    def find_command(self, command_name):
        for command in self.auto_answer:
            if command['command'] == command_name:
                return command

    def find_hidden_lot(self, lot_id):
        for lot in self.hidden_lots:
            if lot == lot_id:
                return lot

config_manager = ConfigManager()