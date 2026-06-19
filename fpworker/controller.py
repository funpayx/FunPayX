from fpx import Message, Order, CurReview
from sqlalchemy import select
from datetime import timedelta, datetime

from utils.config_manager import config_manager
from core.database.engine import Session
from core.database.models import MeetingCooldowns


class FunPayController:
    @staticmethod
    async def MessageManager(message: Message) -> bool:
        '''Фильтр обработки сообщений'''
        if not config_manager.new_message_notifications:
            return False
        if message.sender in config_manager.blacklist_buyers:
            return False
        if config_manager.welcome_msg['enabled']:
            if message.is_system != config_manager.welcome_msg['ignore_system']:
                async with Session() as db:
                    res = await db.execute(select(MeetingCooldowns).where(MeetingCooldowns.chat_id == message.chat_id))
                    cd: MeetingCooldowns = res.scalar_one_or_none()
                    if cd and config_manager.welcome_msg['only_new']:
                        pass
                    elif not cd or (cd.meet_time + timedelta(hours=config_manager.welcome_msg['time']) < datetime.now()):
                        await message.answer(config_manager.welcome_msg['message']) 
                        new_cd = MeetingCooldowns(chat_id=message.chat_id, meet_time=datetime.now())
                        db.add(new_cd)
                        await db.commit()
                        return True
        if config_manager.auto_answer:
            for trigger, answer in config_manager.auto_answer.items():
                if message.text.startswith(trigger):
                    await message.answer(answer)
                    return True
        return True

    @staticmethod
    async def NewOrderManager(order: Order) -> bool:
        if not config_manager.new_order_notifications:
            return False
        if config_manager.auto_issue:
            for trigger, issue in config_manager.auto_issue:
                if trigger in order.description.lower():
                    await order.answer(issue)
                    break
        return True

    @staticmethod
    async def ClosedOrderManager(order: Order) -> bool:
        if not config_manager.closed_order_notifications:
            return False
        return True

    @staticmethod
    async def NewReviewManager(review: CurReview) -> bool:
        if not config_manager.new_review_notifications:
            return False
        if config_manager.review_answer:
            for star, answer in config_manager.review_answer:
                if str(review.stars) == str(star):
                    await review.answer(answer)
                    break
        return True

controller = FunPayController()