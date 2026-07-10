from sqlalchemy import select

from core.database.models import User


class ChatRepo:
    def __init__(self, db):
        self.db = db

    async def get_user_list(self) -> list[User]:
        users = await self.db.execute(select(User))
        return users.scalars().all()