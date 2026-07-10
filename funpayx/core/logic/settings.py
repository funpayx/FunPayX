


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

    @staticmethod
    async def toggle_meeting(action):
        if action == 'meet_user':
            config_manager.welcome_msg['enabled'] = not config_manager.welcome_msg['enabled']
        elif action == 'system':
            config_manager.welcome_msg['ignore_system'] = not config_manager.welcome_msg['ignore_system']
        elif action == 'only_new':
            config_manager.welcome_msg['only_new'] = not config_manager.welcome_msg['only_new']
        await config_manager.update_config()

    @staticmethod
    async def meeting_cooldown(cd):
        config_manager.welcome_msg['time'] = cd
        await config_manager.update_config()

    @staticmethod
    async def meeting_text(text):
        config_manager.welcome_msg['message'] = text
        await config_manager.update_config()
    
    @staticmethod
    async def create_command(command, message):
        config_manager.auto_answer.append(
            {
                'command': command,
                'enabled': True,
                'ping_user': False,
                'message': message                
            }
        )
        await config_manager.update_config()

    @staticmethod
    async def change_cmd_message(command, new_message):
        command = config_manager.find_command(command)
        command['message'] = new_message
        await config_manager.update_config()

    @staticmethod
    async def change_cmd_name(command, new_name):
        command = config_manager.find_command(command)
        command['command'] = new_name
        await config_manager.update_config()
    
    @staticmethod
    async def toggle_command(command, option):
        cmd = config_manager.find_command(command)
        if option == 'enabled':
            cmd['enabled'] = not cmd['enabled']
        elif option == 'notify':
            cmd['ping_user'] = not cmd['ping_user']
        await config_manager.update_config()

    @staticmethod
    async def delete_command(command):
        config_manager.auto_answer = [
        cmd for cmd in config_manager.auto_answer 
        if cmd['command'] != command
        ]
        await config_manager.update_config()

    @staticmethod
    async def toggle_global_settings(option):
        if option == 'raise':
            config_manager.global_settings['auto_raise'] = not config_manager.global_settings['auto_raise']
        elif option == 'delivery':
            config_manager.global_settings['auto_delivery'] = not config_manager.global_settings['auto_delivery']
        elif option == 'answer':
            config_manager.global_settings['auto_answer'] = not config_manager.global_settings['auto_answer']
        await config_manager.update_config()