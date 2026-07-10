from aiogram import Bot

class BotManager:
    _instance: Bot | None = None

    @classmethod
    def init(cls, token: str):
        cls._instance = Bot(token=token)

    @classmethod
    def get(cls) -> Bot:
        if cls._instance is None:
            raise RuntimeError("Бот не инициализирован")
        return cls._instance