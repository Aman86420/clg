from .settings import settings
from .sqlite import get_sqlite_session, init_sqlite_db
from .mongo import get_mongo_db, connect_mongo, close_mongo

async def get_db():
    if settings.DATABASE_TYPE == "sqlite":
        async for session in get_sqlite_session():
            yield session
    else:
        yield await get_mongo_db()

async def init_db():
    if settings.DATABASE_TYPE == "sqlite":
        await init_sqlite_db()
    else:
        await connect_mongo()

async def close_db():
    if settings.DATABASE_TYPE == "mongodb":
        await close_mongo()
