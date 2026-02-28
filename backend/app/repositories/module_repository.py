from sqlalchemy import select
from app.models.sql_models import Module as SQLModule
from app.models.mongo_models import module_helper
from app.config.settings import settings
from bson import ObjectId
from datetime import datetime

class ModuleRepository:
    def __init__(self, db):
        self.db = db
        self.db_type = settings.DATABASE_TYPE
    
    async def create_module(self, user_id: str, title: str, content: str, pdf_text: str = None, video_id: str = None):
        if self.db_type == "sqlite":
            module = SQLModule(user_id=int(user_id), title=title, content=content, pdf_text=pdf_text, video_id=video_id)
            self.db.add(module)
            await self.db.commit()
            await self.db.refresh(module)
            return {"id": str(module.id), "user_id": str(module.user_id), "title": module.title, "content": module.content, "pdf_text": module.pdf_text, "video_id": module.video_id, "created_at": module.created_at}
        else:
            module_doc = {
                "user_id": ObjectId(user_id),
                "title": title,
                "content": content,
                "pdf_text": pdf_text,
                "video_id": video_id,
                "created_at": datetime.utcnow()
            }
            result = await self.db.modules.insert_one(module_doc)
            module_doc["_id"] = result.inserted_id
            return module_helper(module_doc)
    
    async def get_module_by_id(self, module_id: str):
        if self.db_type == "sqlite":
            result = await self.db.execute(select(SQLModule).where(SQLModule.id == int(module_id)))
            module = result.scalar_one_or_none()
            if module:
                return {"id": str(module.id), "user_id": str(module.user_id), "title": module.title, "content": module.content, "pdf_text": module.pdf_text, "video_id": module.video_id, "created_at": module.created_at}
            return None
        else:
            module = await self.db.modules.find_one({"_id": ObjectId(module_id)})
            return module_helper(module) if module else None
    
    async def get_user_modules(self, user_id: str):
        if self.db_type == "sqlite":
            result = await self.db.execute(select(SQLModule).where(SQLModule.user_id == int(user_id)))
            modules = result.scalars().all()
            return [{"id": str(m.id), "user_id": str(m.user_id), "title": m.title, "content": m.content, "pdf_text": m.pdf_text, "video_id": m.video_id, "created_at": m.created_at} for m in modules]
        else:
            cursor = self.db.modules.find({"user_id": ObjectId(user_id)})
            modules = await cursor.to_list(length=100)
            return [module_helper(m) for m in modules]
