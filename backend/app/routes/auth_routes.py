from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schema import UserCreate, UserLogin, Token, UserResponse
from app.repositories.user_repository import UserRepository
from app.utils.auth_utils import hash_password, verify_password
from app.utils.token import create_access_token
from app.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db=Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    new_user = await repo.create_user(user.email, hashed_pwd, user.full_name)
    return new_user

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db=Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_user_by_email(credentials.email)
    
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["id"]})
    return {"access_token": token, "token_type": "bearer"}
