from datetime import datetime

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "hashed_password": user["hashed_password"],
        "full_name": user.get("full_name"),
        "created_at": user.get("created_at", datetime.utcnow())
    }

def module_helper(module) -> dict:
    return {
        "id": str(module["_id"]),
        "user_id": str(module["user_id"]),
        "title": module["title"],
        "content": module["content"],
        "pdf_text": module.get("pdf_text"),
        "video_id": module.get("video_id"),
        "created_at": module.get("created_at", datetime.utcnow())
    }

def result_helper(result) -> dict:
    return {
        "id": str(result["_id"]),
        "user_id": str(result["user_id"]),
        "module_id": str(result["module_id"]),
        "score": result["score"],
        "total_questions": result["total_questions"],
        "time_taken": result.get("time_taken"),
        "created_at": result.get("created_at", datetime.utcnow())
    }
