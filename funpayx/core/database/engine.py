from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.database.models import Base


DATABASE_URL = 'sqlite+aiosqlite:///config.db'
engine = create_async_engine(DATABASE_URL, echo=False)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)