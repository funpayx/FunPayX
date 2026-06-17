


from utils.config_manager import config_manager

class Settings:
    @staticmethod
    async def toggle_notifications():
        config_manager.new_message_notifications = not config_manager.new_message_notifications
        await config_manager.update_config()