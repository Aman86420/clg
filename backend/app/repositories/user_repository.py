from sqlalchemy import select
from app.models.sql_models import User as SQLUser
from app.models.mongo_models import user_helper
from app.config.settings import settings
from bson import ObjectId
from datetime import datetime

class UserRepository:
    def __init__(self, db):
        self.db = db
        self.db_type = settings.DATABASE_TYPE
    
    async def create_user(self, email: str, hashed_password: str, full_name: str = None):
        if self.db_type == "sqlite":
            user = SQLUser(email=email, hashed_password=hashed_password, full_name=full_name)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return {"id": str(user.id), "email": user.email, "full_name": user.full_name, "created_at": user.created_at}
        else:
            user_doc = {
                "email": email,
                "hashed_password": hashed_password,
                "full_name": full_name,
                "created_at": datetime.utcnow()
            }
            result = await self.db.users.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            return user_helper(user_doc)
    
    async def get_user_by_email(self, email: str):
        if self.db_type == "sqlite":
            result = await self.db.execute(select(SQLUser).where(SQLUser.email == email))
            user = result.scalar_one_or_none()
            if user:
                return {"id": str(user.id), "email": user.email, "hashed_password": user.hashed_password, "full_name": user.full_name, "created_at": user.created_at}
            return None
        else:
            user = await self.db.users.find_one({"email": email})
            return user_helper(user) if user else None
    
    async def get_user_by_id(self, user_id: str):
        if self.db_type == "sqlite":
            result = await self.db.execute(select(SQLUser).where(SQLUser.id == int(user_id)))
            user = result.scalar_one_or_none()
            if user:
                return {"id": str(user.id), "email": user.email, "full_name": user.full_name, "created_at": user.created_at}
            return None
        else:
            user = await self.db.users.find_one({"_id": ObjectId(user_id)})
            return user_helper(user) if user else None
