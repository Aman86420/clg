from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.repositories.module_repository import ModuleRepository
from app.services.ai_module_generator import generate_module_with_gemini
from app.routes.upload_routes import get_current_user
from app.config.database import get_db
import httpx
from app.config.settings import settings

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ChatRequest(BaseModel):
    module_id: str
    question: str

@router.post("/ask")
async def ask_chatbot(request: ChatRequest, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    repo = ModuleRepository(db)
    module = await repo.get_module_by_id(request.module_id)
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    context = f"Module: {module['title']}\nContent: {module['content']}\n"
    if module.get('pdf_text'):
        context += f"PDF Text: {module['pdf_text'][:1000]}\n"
    
    prompt = f"{context}\n\nUser Question: {request.question}\n\nAnswer:"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    
    return {"question": request.question, "answer": answer}
