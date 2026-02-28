from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .settings import settings

Base = declarative_base()

engine = create_async_engine(settings.SQLITE_DB_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_sqlite_session():
    async with async_session_maker() as session:
        yield session

async def init_sqlite_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
