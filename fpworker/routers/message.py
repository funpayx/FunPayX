from fpx import Router, Message, Dependency
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape

from client.keyboards.event_menu import message_kb
from fpworker.di_list import get_db
from core.logic.chat import ChatLogic
from fpworker.controller import controller

router = Router()

@router.on_message(custom=controller.MessageManager)
async def get_base_msg(message: Message, db: AsyncSession = Dependency(get_db)):
    chat = ChatLogic(db)
    await chat.message_all_users(
        text=(
            "<b>📩 Новое сообщение</b>\n"
            "━━━━━━━━━━━━━━━━\n"
            f"<b>👤 Отправитель:</b> <code>{escape(message.sender)}</code>\n"
            f"<b>💬 Чат:</b> <code>{escape(str(message.chat_id))}</code>\n"
            f"<b>📝 Текст:</b> <code>{escape(message.text)}</code>\n"
            f"<b>🔧 Тип:</b> {'✅ <b>Системное</b>' if message.is_system else '🔹 <b>Пользовательское</b>'}\n"
            "━━━━━━━━━━━━━━━━\n"
            "<i>Нажми на код, чтобы скопировать</i>"
        ),
        parse_mode='HTML',
        reply_markup=message_kb(message.chat_id)
    )