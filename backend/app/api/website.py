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
        print("=" * 80)
        print("REQUEST URL RECEIVED:", request.url)
        print("=" * 80)

        if provider not in ["groq", "gemini"]:
            raise HTTPException(
               status_code=400,
               detail="Provider must be either 'groq' or 'gemini'."
            )
        # =====================================================
        # Load Website
        # =====================================================

        documents = load_website(request.url)
        print("=" * 80)
        print("DOCUMENT COUNT:", len(documents))
        print("=" * 80)

        for i, doc in enumerate(documents):
            print(f"\nDOCUMENT {i+1}")
            print("SOURCE:", doc.metadata.get("source"))
            print(doc.page_content[:500])

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
        print("=" * 80)
        print("WEBSITE TEXT")
        print(website_text[:5000])
        print("=" * 80)
        # =====================================================
        # Basic Restaurant Website Validation
        # =====================================================

        restaurant_keywords = [
           "restaurant",
           "menu",
           "food",
          "biryani",
          "pizza",
          "burger",
         "dessert",
         "drinks",
         "starter",
         "main course",
         "veg",
         "chicken",
         "paneer",
        ]

        website_lower = website_text.lower()

        if not any(keyword in website_lower for keyword in restaurant_keywords):
            raise HTTPException(
                status_code=400,
                detail="The provided website does not appear to be a restaurant website."
        )
        # Save COMPLETE website for RAG
        set_website_text(website_text)

        # =====================================================
        # Extract Restaurant Profile
        # =====================================================
        # Don't send the entire website to the LLM.
        # Use only a small sample for profile extraction.

        profile_text = website_text[:40000]

        website_profile = extract_restaurant_profile(
            profile_text,
            provider=provider,
        )
        print("=" * 80)
        print("PROFILE LENGTH:", len(profile_text))
        print("PROFILE PREVIEW:")
        print(profile_text[:5000])
        print("=" * 80)

        print("\n🍽 Website Profile")
        print(website_profile)

       # =====================================================
       # Validate Restaurant Website
       # =====================================================

        if not website_profile.get("restaurant_name", "").strip():
            raise HTTPException(
                status_code=400,
                detail="The provided website is not a restaurant website."
      )
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
    # Let FastAPI return original HTTP errors (400, 404, etc.)
    except HTTPException:
        raise

    # Unexpected errors only
    except Exception as e:

        print("\n" + "=" * 80)
        print("❌ WEBSITE LOAD ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail="Internal server error while loading website."
        )