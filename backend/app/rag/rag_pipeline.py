from pathlib import Path

from app.rag.website_loader import load_website
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import create_retriever
from app.rag.keyword_retriever import create_keyword_retriever

from app.services.llm_service import generate_answer


def build_website_rag(url: str):
    """
    Build the Website Knowledge Base and return both
    the Vector Retriever and BM25 Keyword Retriever.
    """

    documents = load_website(url)
    print(f"📄 Documents Loaded: {len(documents)}")

    if not documents:
        raise ValueError("No content could be extracted from the website.")

    chunks = split_documents(documents)
    print(f"✂️ Chunks Created: {len(chunks)}")

    if not chunks:
        raise ValueError("No text chunks were created from the website.")

    # -----------------------------
    # Vector Retriever
    # -----------------------------
    vector_store = create_vector_store(chunks)

    vector_retriever = create_retriever(vector_store)

    # -----------------------------
    # BM25 Keyword Retriever
    # -----------------------------
    keyword_retriever = create_keyword_retriever(chunks)

    print("✅ Website indexed successfully")

    return vector_retriever, keyword_retriever

def ask_question(
    website_retriever,
    website_keyword_retriever,
    pdf_retriever,
    pdf_keyword_retriever,
    provider: str,
    question: str,
):
    """
    Retrieve information using Hybrid Search
    (Vector + BM25) from Website and PDF.
    """

    all_docs = []

    # ==========================================
    # Website Vector Search
    # ==========================================
    if website_retriever is not None:

        docs = website_retriever.invoke(question)

        print(f"🌐 Website Vector Results: {len(docs)}")

        all_docs.extend(docs)

    # ==========================================
    # Website BM25 Search
    # ==========================================
    if website_keyword_retriever is not None:

        docs = website_keyword_retriever.invoke(question)

        print(f"🔑 Website BM25 Results: {len(docs)}")

        all_docs.extend(docs)

    # ==========================================
    # PDF Vector Search
    # ==========================================
    if pdf_retriever is not None:

        docs = pdf_retriever.invoke(question)

        print(f"📄 PDF Vector Results: {len(docs)}")

        all_docs.extend(docs)

    # ==========================================
    # PDF BM25 Search
    # ==========================================
    if pdf_keyword_retriever is not None:

        docs = pdf_keyword_retriever.invoke(question)

        print(f"📑 PDF BM25 Results: {len(docs)}")

        all_docs.extend(docs)

    print(f"🔍 Total Retrieved Documents: {len(all_docs)}")
    if not all_docs:
     return {
        "answer": (
            "I'm designed to answer questions only from the "
            "loaded website or uploaded PDF."
        ),
        "sources": [],
        "confidence": "Low"
    }

    # ==========================================
    # Remove duplicate chunks
    # ==========================================
    unique_docs = []
    seen = set()

    for doc in all_docs:

        text = doc.page_content.strip()

        if text not in seen:
            seen.add(text)
            unique_docs.append(doc)

    # ==========================================
    # Build Context
    # ==========================================
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

    # ==========================================
    # Generate Answer
    # ==========================================
    answer = generate_answer(
        provider=provider,
        context=context,
        question=question,
    )
    # ==========================================
    # Out-of-Domain Detection
    #==========================================

    OUT_OF_DOMAIN_MESSAGE = (
    "I'm designed to answer questions only from the loaded website or uploaded PDF."
)
    if answer.strip() == OUT_OF_DOMAIN_MESSAGE:
      return {
        "answer": answer,
        "sources": [],
        "confidence": "Low"
    }

    # ==========================================
    # Source Attribution
    # ==========================================
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

    # ==========================================
    # Confidence
    # ==========================================
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