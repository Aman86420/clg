from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import init_db, close_db
from app.routes import auth_routes, upload_routes, module_routes, result_routes, chatbot_routes, test_routes

app = FastAPI(title="Learning Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_routes.router)
app.include_router(auth_routes.router)
app.include_router(upload_routes.router)
app.include_router(module_routes.router)
app.include_router(result_routes.router)
app.include_router(chatbot_routes.router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Learning Platform API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
