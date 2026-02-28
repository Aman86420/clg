from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    
mongodb = MongoDB()

async def get_mongo_db():
    return mongodb.client[settings.MONGO_DB_NAME]

async def connect_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URL)

async def close_mongo():
    mongodb.client.close()
