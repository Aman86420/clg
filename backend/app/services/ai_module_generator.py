import httpx
import json
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

async def generate_module_with_gemini(extracted_text: str) -> dict:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        
        prompt = f"""Based on the following text, create a structured learning module with:
1. A clear title
2. Organized content summary (key points)
3. 5 multiple choice questions with 4 options each and correct answer index (0-3)

Text: {extracted_text[:3000]}

Return in this JSON format:
{{
  "title": "Module Title",
  "content": "Detailed summary...",
  "mcqs": [
    {{"question": "Q1?", "options": ["A", "B", "C", "D"], "correct": 0}}
  ]
}}"""
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "candidates" not in data or not data["candidates"]:
                raise ValueError("Invalid response from Gemini API")
            
            text_response = data["candidates"][0]["content"]["parts"][0]["text"]
            start = text_response.find("{")
            end = text_response.rfind("}") + 1
            
            if start == -1 or end == 0:
                raise ValueError("No valid JSON found in Gemini response")
                
            json_str = text_response[start:end]
            return json.loads(json_str)
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Gemini API HTTP error: {e.response.status_code} - {e.response.text}")
        raise Exception(f"Gemini API error: HTTP {e.response.status_code}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
        raise Exception("Invalid response format from Gemini API")
    except Exception as e:
        logger.error(f"Gemini API call failed: {str(e)}")
        raise Exception(f"AI module generation failed: {str(e)}")
