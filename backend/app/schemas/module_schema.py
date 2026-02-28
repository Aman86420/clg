from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModuleCreate(BaseModel):
    title: str
    content: str
    pdf_text: Optional[str] = None
    video_id: Optional[str] = None

class ModuleResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    pdf_text: Optional[str]
    video_id: Optional[str]
    created_at: datetime

class AIModuleRequest(BaseModel):
    extracted_text: str

class AIModuleResponse(BaseModel):
    title: str
    content: str
    mcqs: list
