from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.memory_service import (
    get_website_retriever,
    get_website_keyword_retriever,
    get_pdf_retriever,
    get_pdf_keyword_retriever,
)

from app.services.chat_service import save_chat

from app.rag.rag_pipeline import ask_question

router = APIRouter()


class ChatRequest(BaseModel):
    provider: str = "gemini"
    question: str


@router.post("/")
async def chat(request: ChatRequest):
    """
    Ask a question using the Website Knowledge Base,
    PDF Knowledge Base, or both.
    """

    # Vector Retrievers
    website_retriever = get_website_retriever()
    pdf_retriever = get_pdf_retriever()

    # Keyword Retrievers
    website_keyword_retriever = get_website_keyword_retriever()
    pdf_keyword_retriever = get_pdf_keyword_retriever()

    # Nothing loaded
    if (
        website_retriever is None
        and pdf_retriever is None
        and website_keyword_retriever is None
        and pdf_keyword_retriever is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Please load a website or upload a PDF first."
        )

    # Validate provider
    provider = request.provider.lower()

    if provider not in ["gemini", "groq"]:
        raise HTTPException(
            status_code=400,
            detail="Provider must be either 'gemini' or 'groq'."
        )

    # Generate response
    response = ask_question(
        website_retriever=website_retriever,
        website_keyword_retriever=website_keyword_retriever,
        pdf_retriever=pdf_retriever,
        pdf_keyword_retriever=pdf_keyword_retriever,
        provider=provider,
        question=request.question,
    )

    # Save chat history
    save_chat(
        question=request.question,
        answer=response["answer"]
    )

    return response