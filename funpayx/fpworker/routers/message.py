from fpx import Router, types, Dependency
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape

from client.keyboards.event_menu import message_kb
from fpworker.di_list import get_db
from core.logic.chat import ChatLogic
from fpworker.controller import controller

router = Router()

@router.on_message(custom=controller.MessageManager)
async def get_base_msg(message: types.Message, db: AsyncSession = Dependency(get_db)):
    chat = ChatLogic(db)
    await chat.message_all_users(
        text=(
            f"👤 <b>{escape(message.sender)}:</b> <code>{escape(message.text)}</code>\n"
            f"{'✅ <b>Системное</b>' if message.is_system else '🔹 <b>Пользовательское</b>'}\n"
        ),
        parse_mode='HTML',
        reply_markup=message_kb(message.chat_id)
    )

