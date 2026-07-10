from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.database.engine import Session


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, Session):
        self.Session = Session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.Session() as session:
            data['db'] = session
            return await handler(event, data)

    