from fastapi import APIRouter, Depends, HTTPException
from app.schemas.module_schema import ModuleCreate, ModuleResponse, AIModuleRequest
from app.repositories.module_repository import ModuleRepository
from app.services.ai_module_generator import generate_module_with_gemini
from app.services.youtube_service import search_youtube_video
from app.routes.upload_routes import get_current_user
from app.config.database import get_db
from typing import List

router = APIRouter(prefix="/modules", tags=["Modules"])

@router.post("/", response_model=ModuleResponse)
async def create_module(module: ModuleCreate, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ModuleRepository(db)
    new_module = await repo.create_module(user_id, module.title, module.content, module.pdf_text, module.video_id)
    return new_module

@router.get("/", response_model=List[ModuleResponse])
async def get_my_modules(user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ModuleRepository(db)
    modules = await repo.get_user_modules(user_id)
    return modules

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(module_id: str, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ModuleRepository(db)
    module = await repo.get_module_by_id(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@router.post("/generate-ai")
async def generate_ai_module(request: AIModuleRequest, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    ai_result = await generate_module_with_gemini(request.extracted_text)
    
    video_id = await search_youtube_video(ai_result["title"])
    
    repo = ModuleRepository(db)
    module = await repo.create_module(
        user_id, 
        ai_result["title"], 
        ai_result["content"], 
        request.extracted_text,
        video_id
    )
    
    return {
        "module": module,
        "mcqs": ai_result["mcqs"],
        "video_id": video_id
    }
