import httpx
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

async def search_youtube_video(query: str) -> str:
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 1,
            "key": settings.YOUTUBE_API_KEY
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("items"):
                logger.warning(f"No YouTube videos found for query: {query}")
                return None
                
            return data["items"][0]["id"]["videoId"]
            
    except httpx.HTTPStatusError as e:
        logger.error(f"YouTube API HTTP error: {e.response.status_code} - {e.response.text}")
        raise Exception(f"YouTube API error: HTTP {e.response.status_code}")
    except Exception as e:
        logger.error(f"YouTube API call failed: {str(e)}")
        raise Exception(f"YouTube search failed: {str(e)}")
