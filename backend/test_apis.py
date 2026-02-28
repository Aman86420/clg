import asyncio
import httpx
from app.config.settings import settings

async def test_gemini_api():
    """Test Gemini API connectivity"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": "Hello, respond with 'API Working'"}]}]}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "candidates" in data and data["candidates"]:
                print("[OK] Gemini API: Working")
                return True
            else:
                print("[ERROR] Gemini API: Invalid response format")
                return False
                
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] Gemini API: HTTP {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        print(f"[ERROR] Gemini API: {str(e)}")
        return False

async def test_youtube_api():
    """Test YouTube API connectivity"""
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": "test",
            "type": "video",
            "maxResults": 1,
            "key": settings.YOUTUBE_API_KEY
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data:
                print("[OK] YouTube API: Working")
                return True
            else:
                print("[ERROR] YouTube API: Invalid response format")
                return False
                
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] YouTube API: HTTP {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        print(f"[ERROR] YouTube API: {str(e)}")
        return False

async def main():
    print("Testing API connectivity...\n")
    
    gemini_ok = await test_gemini_api()
    youtube_ok = await test_youtube_api()
    
    print(f"\nResults:")
    print(f"Gemini API: {'OK' if gemini_ok else 'ERROR'}")
    print(f"YouTube API: {'OK' if youtube_ok else 'ERROR'}")
    
    if not gemini_ok or not youtube_ok:
        print("\n[WARNING] Some APIs are not working. Check your API keys in .env file.")

if __name__ == "__main__":
    asyncio.run(main())