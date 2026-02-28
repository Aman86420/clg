import asyncio
import httpx
from app.config.settings import settings

async def list_available_models():
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            print("Available models:")
            if "models" in data:
                for model in data["models"]:
                    print(f"- {model['name']}")
                return True
            else:
                print("No models found")
                return False
                
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] HTTP {e.response.status_code}: {e.response.text}")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(list_available_models())