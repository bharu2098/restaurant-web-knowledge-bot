from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.website import router as website_router
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.history import router as history_router

app = FastAPI(
    title="Restaurant Web Knowledge Bot",
    description="Website RAG + PDF RAG + Hybrid Search + AI Assistant",
    version="1.0.0",
)

# ==========================================================
# CORS Configuration
# ==========================================================

origins = [
    # Local Development
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # Vercel Production
    "https://restaurant-web-knowledge-bot.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# API Routers
# ==========================================================

app.include_router(
    website_router,
    prefix="/website",
    tags=["Website"],
)

app.include_router(
    upload_router,
    prefix="/upload",
    tags=["PDF Upload"],
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)

app.include_router(
    history_router,
    prefix="/history",
    tags=["History"],
)

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Restaurant Web Knowledge Bot API is Running 🚀",
        "version": "1.0.0",
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Restaurant Web Knowledge Bot",
    }