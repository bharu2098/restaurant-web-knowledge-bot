from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.rag_pipeline import build_website_rag
from app.services.memory_service import set_website_retriever

router = APIRouter()


class WebsiteRequest(BaseModel):
    url: str


@router.post("/load")
async def load_website(request: WebsiteRequest):
    """
    Load and index a website into the Website Knowledge Base.
    """

    try:
        retriever = build_website_rag(request.url)

        # Store Website Retriever
        set_website_retriever(retriever)

        return {
            "status": "success",
            "message": "Website indexed successfully.",
            "url": request.url,
            "knowledge_base": "Website"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load website: {str(e)}"
        )