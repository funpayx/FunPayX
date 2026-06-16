from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.engine import Session
from core.database.models import BaseConfig, User

class UserRep:
    def __init__(self, db: AsyncSession, user_id):
        self.uid = user_id
        self.db = db

    async def user(self):
        user = await self.db.execute(select(User).where(User.user_id == self.uid))
        return user.scalar_one_or_none()
    
    async def auth(self):
        new_user = User(user_id=self.uid)
        self.db.add(new_user)
        return new_user