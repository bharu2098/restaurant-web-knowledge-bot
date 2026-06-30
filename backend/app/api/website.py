from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback

from app.rag.website_loader import load_website
from app.rag.rag_pipeline import build_website_rag

from app.services.llm_service import extract_restaurant_profile

from app.services.memory_service import (
    set_website_text,
    set_website_profile,
    set_website_restaurant_name,
    set_website_retriever,
    set_website_keyword_retriever,
)

router = APIRouter()


class WebsiteRequest(BaseModel):
    url: str
    provider: str = "groq"     # Supports both groq and gemini


@router.post("/load")
async def load_website_endpoint(request: WebsiteRequest):
    """
    Load a restaurant website and build the Website Knowledge Base.
    """

    try:
        # =====================================================
        # Validate Provider
        # =====================================================

        provider = request.provider.lower().strip()

        if provider not in ["groq", "gemini"]:
            raise HTTPException(
               status_code=400,
               detail="Provider must be either 'groq' or 'gemini'."
            )
        # =====================================================
        # Load Website
        # =====================================================

        documents = load_website(request.url)

        if not documents:
            raise ValueError(
                "No content could be extracted from the website."
            )

        print(f"📄 Loaded Documents: {len(documents)}")

        # =====================================================
        # Merge Complete Website
        # =====================================================

        website_text = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        # Save COMPLETE website for RAG
        set_website_text(website_text)

        # =====================================================
        # Extract Restaurant Profile
        # =====================================================
        # Don't send the entire website to the LLM.
        # Use only a small sample for profile extraction.

        profile_text = website_text[:8000]

        website_profile = extract_restaurant_profile(
            profile_text,
            provider=provider,
        )

        print("\n🍽 Website Profile")
        print(website_profile)

        # =====================================================
        # Save Profile
        # =====================================================

        set_website_profile(website_profile)

        set_website_restaurant_name(
            website_profile.get(
                "restaurant_name",
                ""
            )
        )

        # =====================================================
        # Build Complete Website RAG
        # =====================================================

        vector_retriever, keyword_retriever = build_website_rag(
            request.url,
            provider=provider,
        )

        # =====================================================
        # Store Retrievers
        # =====================================================

        set_website_retriever(vector_retriever)

        set_website_keyword_retriever(
            keyword_retriever
        )

        # =====================================================
        # Success Response
        # =====================================================

        return {
            "status": "success",
            "message": "Website indexed successfully.",
            "restaurant_name": website_profile.get(
                "restaurant_name",
                "Unknown",
            ),
            "url": request.url,
            "provider":provider,
            "knowledge_base": "Website",
            "pages_loaded": len(documents),
        }

    except Exception as e:

        print("\n" + "=" * 80)
        print("❌ WEBSITE LOAD ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to load website: {str(e)}",
        )