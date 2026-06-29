from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.rag.pdf_loader import load_pdf
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import create_retriever
from app.rag.keyword_retriever import create_keyword_retriever
from app.services.llm_service import (
    extract_restaurant_profile,
)

from app.services.restaurant_validator import (
    validate_restaurant_data,
)

from app.services.memory_service import (
    get_website_profile,
    set_pdf_profile,
    set_pdf_restaurant_name,
    set_pdf_text,
    set_pdf_retriever,
    set_pdf_keyword_retriever,
    set_restaurant_verified,
    set_latest_pdf,
    set_merged_profile,
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a restaurant menu PDF.

    The uploaded PDF is validated against the
    currently loaded restaurant website.
    """

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --------------------------------------------------------
    # Load PDF
    # --------------------------------------------------------

    documents = load_pdf(str(save_path))

    if not documents:
        raise HTTPException(
            status_code=400,
            detail="No content could be extracted from the uploaded PDF."
        )

    pdf_text = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    set_pdf_text(pdf_text)

    # --------------------------------------------------------
    # Extract PDF Restaurant Profile
    # --------------------------------------------------------

    pdf_profile = extract_restaurant_profile(
        pdf_text,
        provider="groq"
    )

    print("\n📄 PDF Profile")
    print(pdf_profile)

    set_pdf_profile(pdf_profile)

    set_pdf_restaurant_name(
        pdf_profile.get("restaurant_name", "")
    )

    set_latest_pdf(file.filename)

    # --------------------------------------------------------
    # Validate Against Website
    # --------------------------------------------------------

    website_profile = get_website_profile()
    set_restaurant_verified(False)
    if website_profile:

        validation = validate_restaurant_data(
            pdf_profile,
            website_profile,
        )

        if not validation["valid"]:
            set_restaurant_verified(False)
            raise HTTPException(
                status_code=400,
                detail={
                    "message": validation["message"],
                    "conflicts": validation["conflicts"]
                }
            )

        set_restaurant_verified(True)
        # ========================================================
        # Merge Website + PDF
        # ========================================================

        merged_profile = website_profile.copy()

        #  Latest PDF becomes source of truth
        merged_profile["menu"] = pdf_profile.get("menu", {})

        if pdf_profile.get("timings"):
         merged_profile["timings"] = pdf_profile["timings"]

        if pdf_profile.get("phone"):
         merged_profile["phone"] = pdf_profile["phone"]

        if pdf_profile.get("email"):
          merged_profile["email"] = pdf_profile["email"]

        if pdf_profile.get("address"):
         merged_profile["address"] = pdf_profile["address"]

        set_merged_profile(merged_profile)

        print("\n✅ Merged Restaurant Profile")
        print(merged_profile)
    else:
        # No website has been loaded.
        # Use the PDF as the only knowledge source.
        set_restaurant_verified(False)
        set_merged_profile(pdf_profile)
    # --------------------------------------------------------
    # Build PDF RAG
    # --------------------------------------------------------

    chunks = split_documents(documents)


    import uuid

    persist_dir = f"chroma_db_pdf/{uuid.uuid4()}"

    vector_store = create_vector_store(
        chunks,
        persist_directory=persist_dir,
        collection_name="pdf_collection",
    )

    vector_retriever = create_retriever(
        vector_store
    )

    keyword_retriever = create_keyword_retriever(
       chunks
)

    set_pdf_retriever(vector_retriever)

    set_pdf_keyword_retriever(
        keyword_retriever
    )

    print("✅ PDF Knowledge Base Loaded")

    return {
        "status": "success",
        "message": "PDF uploaded successfully.",
        "restaurant_name": pdf_profile.get(
            "restaurant_name",
            ""
        ),
        "verified": website_profile is not None,
        "merged": website_profile is not None,
        "knowledge_base": "PDF",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }