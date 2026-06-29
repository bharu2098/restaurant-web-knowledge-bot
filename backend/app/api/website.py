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


@router.post("/load")
async def load_website_endpoint(request: WebsiteRequest):
    """
    Load a restaurant website and build the Website Knowledge Base.
    """

    try:

        # =====================================================
        # Clear previous restaurant information
        # =====================================================


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
        # Merge Website Text
        # =====================================================

        website_text = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        # Save website text
        set_website_text(website_text)

        # =====================================================
        # Extract Restaurant Profile
        # =====================================================

        website_profile = extract_restaurant_profile(
            website_text,
            provider = "groq"
        )

        print("\n🍽 Website Profile")
        print(website_profile)

        # Save Profile
        set_website_profile(website_profile)

        # Save Restaurant Name
        set_website_restaurant_name(
            website_profile.get(
                "restaurant_name",
                ""
            )
        )

        # =====================================================
        # Build Website RAG
        # =====================================================

        vector_retriever, keyword_retriever = build_website_rag(
            request.url
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
                "Unknown"
            ),
            "url": request.url,
            "knowledge_base": "Website"
        }

    except Exception as e:

        print("\n" + "=" * 80)
        print("❌ WEBSITE LOAD ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to load website: {str(e)}"
    )