from sqlalchemy import select
from app.models.sql_models import Result as SQLResult
from app.models.mongo_models import result_helper
from app.config.settings import settings
from bson import ObjectId
from datetime import datetime

class ResultRepository:
    def __init__(self, db):
        self.db = db
        self.db_type = settings.DATABASE_TYPE
    
    async def create_result(self, user_id: str, module_id: str, score: float, total_questions: int, time_taken: int = None):
        if self.db_type == "sqlite":
            result = SQLResult(user_id=int(user_id), module_id=int(module_id), score=score, total_questions=total_questions, time_taken=time_taken)
            self.db.add(result)
            await self.db.commit()
            await self.db.refresh(result)
            return {"id": str(result.id), "user_id": str(result.user_id), "module_id": str(result.module_id), "score": result.score, "total_questions": result.total_questions, "time_taken": result.time_taken, "created_at": result.created_at}
        else:
            result_doc = {
                "user_id": ObjectId(user_id),
                "module_id": ObjectId(module_id),
                "score": score,
                "total_questions": total_questions,
                "time_taken": time_taken,
                "created_at": datetime.utcnow()
            }
            result = await self.db.results.insert_one(result_doc)
            result_doc["_id"] = result.inserted_id
            return result_helper(result_doc)
    
    async def get_user_results(self, user_id: str):
        if self.db_type == "sqlite":
            result = await self.db.execute(select(SQLResult).where(SQLResult.user_id == int(user_id)))
            results = result.scalars().all()
            return [{"id": str(r.id), "user_id": str(r.user_id), "module_id": str(r.module_id), "score": r.score, "total_questions": r.total_questions, "time_taken": r.time_taken, "created_at": r.created_at} for r in results]
        else:
            cursor = self.db.results.find({"user_id": ObjectId(user_id)})
            results = await cursor.to_list(length=100)
            return [result_helper(r) for r in results]
    
    async def get_module_results(self, module_id: str):
        if self.db_type == "sqlite":
            result = await self.db.execute(select(SQLResult).where(SQLResult.module_id == int(module_id)))
            results = result.scalars().all()
            return [{"id": str(r.id), "user_id": str(r.user_id), "module_id": str(r.module_id), "score": r.score, "total_questions": r.total_questions, "time_taken": r.time_taken, "created_at": r.created_at} for r in results]
        else:
            cursor = self.db.results.find({"module_id": ObjectId(module_id)})
            results = await cursor.to_list(length=100)
            return [result_helper(r) for r in results]
