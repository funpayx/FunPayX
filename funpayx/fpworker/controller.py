from fpx import types
from sqlalchemy import select
from datetime import timedelta, datetime

from utils.config_manager import config_manager
from core.database.engine import Session
from core.logic.chat import ChatLogic
from core.database.models import MeetingCooldowns


class FunPayController:
    @staticmethod
    async def MessageManager(message: types.Message) -> bool:
        '''Фильтр обработки сообщений'''
        if not config_manager.new_message_notifications:
            return False
        if message.sender in config_manager.blacklist_buyers:
            return False
        welcome = config_manager.welcome_msg
        if (
            welcome.get('enabled')
            and config_manager.global_settings.get('auto_answer')
            and message.is_system != welcome.get('ignore_system')
        ):
            async with Session() as db:
                res = await db.execute(
                    select(MeetingCooldowns).where(MeetingCooldowns.chat_id == message.chat_id)
                )
                cd: MeetingCooldowns | None = res.scalar_one_or_none()
                now = datetime.now()
                should_send = False
                if not cd:
                    db.add(MeetingCooldowns(chat_id=message.chat_id, meet_time=now))
                    should_send = True
                elif not welcome.get('only_new'):
                    if cd.meet_time + timedelta(hours=welcome['time']) < now:
                        cd.meet_time = now
                        should_send = True
                if should_send:
                    await message.answer(welcome['message'])
                    await db.commit()
        cmd = config_manager.find_command(message.text)
        if cmd and config_manager.global_settings['auto_answer'] and cmd['enabled']: 
            if cmd['ping_user']:
                async with Session() as db:
                    chat = ChatLogic(db)
                    await chat.message_all_users(
                        text=(
                            f'Вызвана команда {cmd['command']}\n'
                        )
                    )
            await message.answer(cmd['message'])
        return True

    @staticmethod
    async def NewOrderManager(order: types.Order) -> bool:
        if not config_manager.new_order_notifications:
            return False
        if config_manager.global_settings['auto_delivery']:
            if config_manager.auto_issue:
                for trigger, issue in config_manager.auto_issue:
                    if trigger in order.description.lower():
                        await order.answer(issue)
                        break
        return True

    @staticmethod
    async def ClosedOrderManager(order: types.Order) -> bool:
        if not config_manager.closed_order_notifications:
            return False
        return True

    @staticmethod
    async def NewReviewManager(review: types.CurReview) -> bool:
        if not config_manager.new_review_notifications:
            return False
        if config_manager.review_answer:
            for star, answer in config_manager.review_answer:
                if str(review.stars) == str(star):
                    await review.answer(answer)
                    break
        return True

controller = FunPayController()