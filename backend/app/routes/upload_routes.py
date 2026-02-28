from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header
from app.services.pdf_parser import extract_text_from_pdf
from app.utils.token import verify_token
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("app/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    try:
        # Validate file type
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")
        
        # Ensure upload directory exists
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded file
        file_path = UPLOAD_DIR / f"{user_id}_{file.filename}"
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            logger.error(f"File save error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Extract text from PDF
        try:
            extracted_text = await extract_text_from_pdf(str(file_path))
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="PDF appears to be empty or unreadable")
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            # Clean up file on extraction failure
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(status_code=500, detail=f"Failed to extract text from PDF: {str(e)}")
        
        return {
            "filename": file.filename,
            "file_path": str(file_path),
            "extracted_text": extracted_text[:500],
            "full_text_length": len(extracted_text)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload_pdf: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
