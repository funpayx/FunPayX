from fpx import Router, types, Dependency
from sqlalchemy.ext.asyncio import AsyncSession

from fpworker.di_list import get_db
from core.logic.chat import ChatLogic
from fpworker.controller import controller
from client.keyboards.event_menu import get_order_keyboard


router = Router()

@router.on_new_order()
async def handle_new_order(order: types.Order, db: AsyncSession = Dependency(get_db)):
    if await controller.NewOrderManager(order) is True:
        chat = ChatLogic(db)
        await chat.message_all_users(
            text=(
                f"💰 <b>Новый заказ:</b> {order.name}\n"
                f"🙍‍♂️ <b>Покупатель:</b> {order.client_name}\n"
                f"💵 <b>Сумма:</b> {order.price} ₽\n"
                f"📇 <b>ID:</b> <code>#{order.order_id}</code>\n"
            ),
            parse_mode='HTML',
            reply_markup=get_order_keyboard(order.order_id, order.chat_id)
        )

@router.on_confirmed_orders()
async def handle_closed_order(order: types.Order, db: AsyncSession = Dependency(get_db)):
    if await controller.ClosedOrderManager(order) is True:
        chat = ChatLogic(db)
        await chat.message_all_users(
            text=f'🌕 Пользователь <a href="https://funpay.com/users/{order.chat_id}/">{order.client_name}</a> подтвердил выполнение заказа <code>{order.order_id}</code>. (<code>{order.price} ₽</code>)',
            parse_mode='HTML',
            reply_markup=get_order_keyboard(order.order_id, order.chat_id)
        )