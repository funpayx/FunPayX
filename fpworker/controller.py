from fpx import Message, Order, CurReview

from utils.config_manager import config_manager


class FunPayController:
    @staticmethod
    async def MessageManager(message: Message) -> bool:
        '''Фильтр обработки сообщений'''
        if not config_manager.new_message_notifications:
            return False
        if message.sender in config_manager.blacklist_buyers:
            return False
        if config_manager.auto_answer:
            for trigger, answer in config_manager.auto_answer:
                if message.text.startswith(trigger):
                    await message.answer(answer)
                    break
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