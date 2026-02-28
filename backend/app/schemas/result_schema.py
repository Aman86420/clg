from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResultCreate(BaseModel):
    module_id: str
    score: float
    total_questions: int
    time_taken: Optional[int] = None

class ResultResponse(BaseModel):
    id: str
    user_id: str
    module_id: str
    score: float
    total_questions: int
    time_taken: Optional[int]
    created_at: datetime

class MCQSubmission(BaseModel):
    module_id: str
    answers: list[int]
    time_taken: Optional[int] = None
