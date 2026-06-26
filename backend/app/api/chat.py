from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.memory_service import (
    get_website_retriever,
    get_pdf_retriever,
)
from app.rag.rag_pipeline import ask_question

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def chat(request: ChatRequest):
    """
    Ask a question using the Website Knowledge Base,
    PDF Knowledge Base, or both.
    """

    website_retriever = get_website_retriever()
    pdf_retriever = get_pdf_retriever()

    # Nothing loaded
    if website_retriever is None and pdf_retriever is None:
        raise HTTPException(
            status_code=400,
            detail="Please load a website or upload a PDF first."
        )

    response = ask_question(
        website_retriever=website_retriever,
        pdf_retriever=pdf_retriever,
        question=request.question,
    )

    return response