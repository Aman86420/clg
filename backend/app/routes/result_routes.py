from fastapi import APIRouter, Depends, HTTPException
from app.schemas.result_schema import ResultResponse, MCQSubmission
from app.repositories.result_repository import ResultRepository
from app.repositories.module_repository import ModuleRepository
from app.services.mcq_generator import calculate_score
from app.services.result_analyzer import analyze_results
from app.routes.upload_routes import get_current_user
from app.config.database import get_db
from typing import List

router = APIRouter(prefix="/results", tags=["Results"])

@router.post("/submit-mcq", response_model=ResultResponse)
async def submit_mcq(submission: MCQSubmission, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    module_repo = ModuleRepository(db)
    module = await module_repo.get_module_by_id(submission.module_id)
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    correct_answers = [0, 1, 2, 0, 1]
    score = calculate_score(submission.answers, correct_answers)
    
    result_repo = ResultRepository(db)
    result = await result_repo.create_result(
        user_id, 
        submission.module_id, 
        score, 
        len(correct_answers),
        submission.time_taken
    )
    
    return result

@router.get("/my-results", response_model=List[ResultResponse])
async def get_my_results(user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ResultRepository(db)
    results = await repo.get_user_results(user_id)
    return results

@router.get("/module/{module_id}", response_model=List[ResultResponse])
async def get_module_results(module_id: str, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ResultRepository(db)
    results = await repo.get_module_results(module_id)
    return results

@router.get("/analytics")
async def get_analytics(user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ResultRepository(db)
    results = await repo.get_user_results(user_id)
    analytics = analyze_results(results)
    return analytics
