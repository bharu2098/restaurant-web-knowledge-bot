from fastapi import FastAPI

from app.api.website import router as website_router
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router

app = FastAPI(
    title="Restaurant Web Knowledge Bot",
    description="Web Knowledge Bot with PDF RAG",
    version="1.0.0"
)

# Website API
app.include_router(
    website_router,
    prefix="/website",
    tags=["Website"]
)

# PDF Upload API
app.include_router(
    upload_router,
    prefix="/upload",
    tags=["PDF Upload"]
)

# Chat API
app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Restaurant Web Knowledge Bot API is Running 🚀"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }