


from utils.config_manager import config_manager

class Settings:
    @staticmethod
    async def toggle_notifications(option):
        if option == 'toggle_messages':
            config_manager.new_message_notifications = not config_manager.new_message_notifications
        elif option == 'toggle_new_orders':
            config_manager.new_order_notifications = not config_manager.new_order_notifications
        elif option == 'toggle_closed_orders':
            config_manager.closed_order_notifications = not config_manager.closed_order_notifications
        elif option == 'toggle_refunded_orders':
            config_manager.refunded_order_notifications = not config_manager.refunded_order_notifications
        elif option == 'toggle_new_reviews':
            config_manager.new_review_notifications = not config_manager.new_review_notifications
        await config_manager.update_config()

    @staticmethod
    async def toggle_user_msg_filter(user_name):
        '''Удаляет/Добавляет из блеклиста имя юзера'''
        if user_name in config_manager.blacklist_buyers:
            config_manager.blacklist_buyers.remove(user_name)
        else:
            config_manager.blacklist_buyers.append(user_name)
        await config_manager.update_config()