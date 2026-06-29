from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

from app.services.memory_service import (
    get_website_retriever,
    get_website_keyword_retriever,
    get_pdf_retriever,
    get_pdf_keyword_retriever,
    get_pdf_profile,
    is_restaurant_verified,
)

from app.services.chat_service import (
    save_chat,
    get_recent_chat_history,
)

from app.rag.rag_pipeline import ask_question

router = APIRouter()


class ChatRequest(BaseModel):
    provider: str = "gemini"
    question: str


# ==========================================
# Greeting Words
# ==========================================

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "hii",
    "helo",
    "good morning",
    "good afternoon",
    "good evening",
}


# ==========================================
# Greeting Responses
# ==========================================

GREETING_MESSAGES = [
    "👋 Welcome to Xotic Restaurant!\n\nHow can I help you today?",

    "😊 Hi! Welcome to Xotic Restaurant.\n\nWhat would you like to know today?",

    "🍽️ Welcome! I'm your Restaurant AI Assistant.\n\nFeel free to ask me about our menu, prices or restaurant.",

    "👋 Hello there!\n\nI'm here to help you with our menu, timings, prices and restaurant information.",

    "😊 Hi! Thanks for visiting Xotic Restaurant.\n\nHow may I assist you today?",
]


@router.post("/")
async def chat(request: ChatRequest):
    """
    Restaurant AI Chat Endpoint
    """

    # ==========================================
    # Clean Question
    # ==========================================

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # ==========================================
    # Greeting Handling
    # ==========================================

    if question.lower() in GREETINGS:

        greeting_answer = random.choice(GREETING_MESSAGES)

        save_chat(
            question=question,
            answer=greeting_answer
        )

        return {
            "answer": greeting_answer,
            "sources": [],
            "confidence": "High",
            "provider": "system",
        }

    # ==========================================
    # Validate Provider
    # ==========================================

    provider = request.provider.lower()

    if provider not in ["gemini", "groq"]:
        raise HTTPException(
            status_code=400,
            detail="Provider must be either 'gemini' or 'groq'."
        )

    # ==========================================
    # Get Knowledge Bases
    # ==========================================

    website_retriever = get_website_retriever()
    website_keyword_retriever = get_website_keyword_retriever()

    pdf_retriever = get_pdf_retriever()
    pdf_keyword_retriever = get_pdf_keyword_retriever()

    # ==========================================
    # Ensure Knowledge Exists
    # ==========================================

    if (
        website_retriever is None
        and website_keyword_retriever is None
        and pdf_retriever is None
        and pdf_keyword_retriever is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Please load a website or upload a PDF first."
        )
    # ==========================================
    # Restaurant Validation
    # ==========================================

    if website_retriever is not None and pdf_retriever is not None:
        if not is_restaurant_verified():
            raise HTTPException(
                status_code=400,
                detail=(
                "The uploaded menu PDF does not belong to the loaded restaurant."
                )
           )
        

    # ==========================================
    # Exact Menu Lookup
    # ==========================================

    # ==========================================
    # Exact Menu Lookup
    # ==========================================

    pdf_profile = get_pdf_profile()

    if pdf_profile and "menu" in pdf_profile:

      menu = pdf_profile["menu"]
      question_lower = question.lower()

      for item, price in menu.items():

         if item.lower() in question_lower:

            if (
                "price" in question_lower
                or "cost" in question_lower
                or "how much" in question_lower
            ):
                return {
                    "answer": f"The price of {item} is {price}.",
                    "sources": [],
                    "confidence": "High",
                    "provider": provider,
                }

            if (
                "have" in question_lower
                or "available" in question_lower
                or "serve" in question_lower
                or "do you have" in question_lower
            ):
                return {
                    "answer": f"Yes, we serve {item}. It costs {price}.",
                    "sources": [],
                    "confidence": "High",
                    "provider": provider,
                }



    # ==========================================
    # Conversation History
    # ==========================================

    conversation_history = get_recent_chat_history(limit=5)

    # ==========================================
    # Ask RAG
    # ==========================================

    response = ask_question(
        website_retriever=website_retriever,
        website_keyword_retriever=website_keyword_retriever,
        pdf_retriever=pdf_retriever,
        pdf_keyword_retriever=pdf_keyword_retriever,
        provider=provider,
        question=question,
        conversation_history=conversation_history,
    )

    # ==========================================
    # Save Chat
    # ==========================================

    save_chat(
        question=question,
        answer=response["answer"]
    )

    # ==========================================
    # Return Response
    # ==========================================

    return {
        "answer": response["answer"],
        "sources": response.get("sources", []),
        "confidence": response.get("confidence", "High"),
        "provider": provider,
    }