from pathlib import Path

from app.rag.website_loader import load_website
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import create_retriever
from app.services.gemini_service import generate_answer


def build_website_rag(url: str):
    """
    Build the Website Knowledge Base and return a retriever.
    """

    documents = load_website(url)
    print(f"📄 Documents Loaded: {len(documents)}")

    if not documents:
        raise ValueError("No content could be extracted from the website.")

    chunks = split_documents(documents)
    print(f"✂️ Chunks Created: {len(chunks)}")

    if not chunks:
        raise ValueError("No text chunks were created from the website.")

    vector_store = create_vector_store(chunks)

    retriever = create_retriever(vector_store)

    print("✅ Website indexed successfully")

    return retriever


def ask_question(
    website_retriever,
    pdf_retriever,
    question: str,
):
    """
    Retrieve information from Website Knowledge,
    PDF Knowledge, or both.
    """

    website_docs = []
    pdf_docs = []

    # -------------------------------
    # Retrieve Website Knowledge
    # -------------------------------
    if website_retriever is not None:

        website_docs = website_retriever.invoke(question)

        print(f"🌐 Website Documents Retrieved: {len(website_docs)}")

    # -------------------------------
    # Retrieve PDF Knowledge
    # -------------------------------
    if pdf_retriever is not None:

        pdf_docs = pdf_retriever.invoke(question)

        print(f"📄 PDF Documents Retrieved: {len(pdf_docs)}")

    all_docs = website_docs + pdf_docs

    print(f"🔍 Total Retrieved Documents: {len(all_docs)}")

    if not all_docs:
        return {
            "answer": "I couldn't find any relevant information in the loaded website or uploaded PDF.",
            "sources": [],
            "confidence": "Low"
        }

    # -------------------------------
    # Remove Duplicate Chunks
    # -------------------------------
    unique_docs = []
    seen = set()

    for doc in all_docs:

        text = doc.page_content.strip()

        if text not in seen:

            seen.add(text)
            unique_docs.append(doc)

    # -------------------------------
    # Build Separate Context
    # -------------------------------
    website_context = []
    pdf_context = []

    for doc in unique_docs:

        source = doc.metadata.get("source", "")

        if source.startswith("http"):

            website_context.append(doc.page_content)

        else:

            pdf_context.append(doc.page_content)

    context = f"""
================ WEBSITE KNOWLEDGE ================

{chr(10).join(website_context)}

================ PDF KNOWLEDGE ====================

{chr(10).join(pdf_context)}
"""

    # -------------------------------
    # Generate Answer
    # -------------------------------
    answer = generate_answer(
        context=context,
        question=question
    )

    # -------------------------------
    # Source Attribution
    # -------------------------------
    sources = []
    added = set()

    for doc in unique_docs:

        metadata = doc.metadata

        source = metadata.get("source", "")

        if source.startswith("http"):

            key = ("Website", source)

            if key not in added:

                added.add(key)

                sources.append({
                    "type": "Website",
                    "url": source
                })

        else:

            filename = Path(source).name if source else "Unknown PDF"

            page = metadata.get("page")

            key = ("PDF", filename, page)

            if key not in added:

                added.add(key)

                sources.append({
                    "type": "PDF",
                    "file": filename,
                    "page": page + 1 if page is not None else None
                })

    # -------------------------------
    # Confidence
    # -------------------------------
    total_docs = len(unique_docs)

    if total_docs >= 5:
        confidence = "High"
    elif total_docs >= 3:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }