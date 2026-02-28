from fastapi import APIRouter, UploadFile, File, Depends
from app.services.pdf_parser import extract_text_from_pdf
from app.services.ai_module_generator import generate_module_with_gemini
from app.services.youtube_service import search_youtube_video
from app.repositories.module_repository import ModuleRepository
from app.config.database import get_db
from pathlib import Path
import shutil

router = APIRouter(prefix="/test", tags=["Testing - No Auth"])

UPLOAD_DIR = Path("app/storage/uploads")

@router.post("/upload-and-generate")
async def upload_and_generate_module(file: UploadFile = File(...), db=Depends(get_db)):
    """
    Upload PDF → Extract Text → Generate AI Module → Get YouTube Video
    Returns: module with video_id
    """
    # Save PDF
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text
    extracted_text = await extract_text_from_pdf(str(file_path))
    
    # Generate AI module
    ai_result = await generate_module_with_gemini(extracted_text)
    
    # Get YouTube video
    video_id = await search_youtube_video(ai_result["title"])
    
    # Save to database (using dummy user_id = "1")
    repo = ModuleRepository(db)
    module = await repo.create_module(
        user_id="1",
        title=ai_result["title"],
        content=ai_result["content"],
        pdf_text=extracted_text[:1000],
        video_id=video_id
    )
    
    return {
        "module": module,
        "mcqs": ai_result["mcqs"],
        "video_id": video_id,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else None
    }

@router.get("/search-video")
async def search_video(query: str):
    """
    Simple YouTube search test
    Example: /test/search-video?query=python tutorial
    """
    video_id = await search_youtube_video(query)
    return {
        "query": query,
        "video_id": video_id,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else None
    }
