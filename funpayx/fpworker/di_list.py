

from core.database.engine import Session


async def get_db(event=None):
    async with Session() as db:
        yield db