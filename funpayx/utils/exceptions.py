class BotError(Exception):
    def __init__(self, message='Произошла ошибка в боте'):
        self.message = message
        super().__init__(self.message)

class InvalidPassword(BotError):
    '''Неправильный пароль введён'''
    pass

class UserAlreadyRegistered(BotError):
    '''Юзер уже зарегестрирован'''
    pass