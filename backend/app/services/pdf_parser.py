import pdfplumber
import logging

logger = logging.getLogger(__name__)

async def extract_text_from_pdf(file_path: str) -> str:
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {str(e)}")
                    continue
        
        if not text.strip():
            raise ValueError("No readable text found in PDF")
            
        return text.strip()
        
    except Exception as e:
        logger.error(f"PDF extraction failed for {file_path}: {str(e)}")
        raise Exception(f"PDF processing error: {str(e)}")
