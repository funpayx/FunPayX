from sqlalchemy.ext.asyncio import AsyncSession

from core.logic.repo.user_repo import UserRep
from config import PASSWORD
from utils import exceptions as err

class UserLogic:
    def __init__(self, db: AsyncSession, user_id: int | str):
        self.user_id = user_id
        self.repo = UserRep(db, user_id)
        self.db = db

    async def is_authorized(self):
        user = await self.repo.user()
        return user

    async def auth(self, user_pass):
        if user_pass != PASSWORD:
            raise err.InvalidPassword('Ты ввёл неверный пароль!')
        if await self.is_authorized():
            raise err.UserAlreadyRegistered('Вы уже авторизованы в системе.')
        new_user = await self.repo.auth()
        await self.db.commit()
        return True