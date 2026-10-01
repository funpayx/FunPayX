class BotError(Exception):
    def __init__(self, message='Произошла ошибка в боте'):
        self.message = message
        super().__init__(self.message)


class FunPayXError(Exception):
    def __init__(self, message='Произошла ошибка внутри проекта'):
        self.message = message
        super().__init__(self.message)


class InvalidPassword(BotError):
    '''Неправильный пароль введён'''
    def __init__(self, message='Неправильный пароль введён'):
        super().__init__(message)


class UserAlreadyRegistered(BotError):
    '''Юзер уже зарегестрирован'''
    def __init__(self, message='Юзер уже зарегестрирован'):
        super().__init__(message)


class PasswordNotSetError(FunPayXError):
    '''Пароль в .env не задан'''
    def __init__(self, message='Пароль в .env не задан'):
        super().__init__(message)
