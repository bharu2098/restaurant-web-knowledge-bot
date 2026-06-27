from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.rag.pdf_loader import load_pdf
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import create_retriever
from app.rag.keyword_retriever import create_keyword_retriever

from app.services.memory_service import (
    set_pdf_retriever,
    set_pdf_keyword_retriever,
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF and index it into the PDF Knowledge Base.
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load PDF
    documents = load_pdf(str(save_path))

    if not documents:
        raise HTTPException(
            status_code=400,
            detail="No content could be extracted from the uploaded PDF."
        )

    # Split into chunks
    chunks = split_documents(documents)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No text chunks could be created from the uploaded PDF."
        )

    # --------------------------------
    # Vector Retriever
    # --------------------------------
    vector_store = create_vector_store(chunks)

    vector_retriever = create_retriever(vector_store)

    # --------------------------------
    # Keyword Retriever (BM25)
    # --------------------------------
    keyword_retriever = create_keyword_retriever(chunks)

    # Store Vector Retriever
    set_pdf_retriever(vector_retriever)

    # Store Keyword Retriever
    set_pdf_keyword_retriever(keyword_retriever)

    return {
        "status": "success",
        "message": "PDF uploaded and indexed successfully.",
        "knowledge_base": "PDF",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }