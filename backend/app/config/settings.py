from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    DATABASE_TYPE: Literal["sqlite", "mongodb"] = "sqlite"
    SQLITE_DB_URL: str = "sqlite+aiosqlite:///./app.db"
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "learning_platform"
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    GEMINI_API_KEY: str
    YOUTUBE_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
