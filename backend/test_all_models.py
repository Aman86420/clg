import asyncio
import httpx
from app.config.settings import settings

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro", 
    "gemini-1.0-pro",
    "gemini-pro"
]

async def test_gemini_model(model_name):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "candidates" in data and data["candidates"]:
                print(f"[OK] {model_name}: Working")
                return True
            else:
                print(f"[ERROR] {model_name}: Invalid response")
                return False
                
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] {model_name}: HTTP {e.response.status_code}")
        return False
    except Exception as e:
        print(f"[ERROR] {model_name}: {str(e)}")
        return False

async def main():
    print("Testing all Gemini models...\n")
    
    working_models = []
    for model in models_to_test:
        if await test_gemini_model(model):
            working_models.append(model)
    
    print(f"\nWorking models: {working_models if working_models else 'None'}")

if __name__ == "__main__":
    asyncio.run(main())