import logging
from aiogram import Router, F
from aiogram.types import ErrorEvent
from utils.exceptions import BotError

router = Router()

@router.error()
async def global_error_handler(event: ErrorEvent):
    if isinstance(event.exception, BotError):
        message_text = event.exception.message
        if event.update.callback_query:
            await event.update.callback_query.answer(message_text, show_alert=True)
        elif event.update.message:
            await event.update.message.answer(f"❌ {message_text}")
        return
    logging.error(f"Критическая ошибка: {event.exception}", exc_info=True)
    if event.update.callback_query:
        await event.update.callback_query.answer("Произошла ошибка на сервере", show_alert=True)