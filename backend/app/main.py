from fastapi import FastAPI

app = FastAPI(
    title="Restaurant Web Knowledge Bot",
    description="Web Knowledge Bot with PDF RAG",
    version="1.0.0"
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