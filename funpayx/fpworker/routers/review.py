from fpx import Router, types, Dependency
from sqlalchemy.ext.asyncio import AsyncSession

from fpworker.di_list import get_db
from core.logic.chat import ChatLogic
from fpworker.controller import controller
from client.keyboards.event_menu import get_order_keyboard

router = Router()

@router.on_new_review()
async def handle_new_review(review: types.CurReview, db: AsyncSession = Dependency(get_db)):
    if await controller.NewReviewManager(review) is True:
        chat = ChatLogic(db)
        await chat.message_all_users(
            text=f'🔮 Вы получили {'⭐' * int(review.stars)} за заказ <code>{review.order_id}</code>!\n\n💬 <b>Отзыв:</b>\n<code>{review.text}</code>',
            reply_markup=get_order_keyboard(review.order_id, review.order.chat_id),
            parse_mode='HTML'
        )
