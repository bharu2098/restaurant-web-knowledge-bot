from pathlib import Path
import shutil

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
  
    website_db = Path("chroma_db_website")

    if website_db.exists():
        shutil.rmtree(website_db)

    vector_store = create_vector_store(
        chunks,
        persist_directory="chroma_db_website",
        collection_name="website_collection",
)

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
    conversation_history=None,
):
    """
    Retrieve information using Hybrid Search
    (Vector + BM25) from Website and PDF.
    """

    all_docs = []

    # ==========================================
    # Build Retrieval Query
    # ==========================================

    retrieval_query = question.lower()

    # Add previous question for follow-up questions
    if conversation_history and len(conversation_history) > 0:
        last_question = conversation_history[-1]["question"]
        retrieval_query = f"{last_question}\n{retrieval_query}"

    # Restaurant-specific query expansion
    if "menu" in retrieval_query:
        retrieval_query += " menu food dishes"

    if (
    "drink" in retrieval_query
    or "drinks" in retrieval_query
    or "beverage" in retrieval_query
    or "beverages" in retrieval_query
):
     retrieval_query += (
        " drinks beverages "
        "seasonal fresh juices "
        "lassi "
        "falooda "
        "fresh lime water "
        "fresh lime soda "
        "coke "
        "fanta "
        "sprite "
        "thums up"
    )

    if "dessert" in retrieval_query or "sweet" in retrieval_query:
        retrieval_query += " dessert sweets gulab jamun ice cream"

    if "starter" in retrieval_query:
        retrieval_query += " starters appetizer spring rolls paneer tikka chicken wings"

    if "biryani" in retrieval_query:
        retrieval_query += " veg biryani chicken biryani"

    if "price" in retrieval_query or "cost" in retrieval_query:
        retrieval_query += " rs price cost"

    if "timing" in retrieval_query or "open" in retrieval_query or "close" in retrieval_query:
        retrieval_query += " opening hours timings"

    if "address" in retrieval_query or "location" in retrieval_query:
        retrieval_query += " address location"

    if "special" in retrieval_query or "best" in retrieval_query or "recommended" in retrieval_query:
        retrieval_query += " popular menu signature recommended dishes"

    if "veg" in retrieval_query or "vegetarian" in retrieval_query:
      retrieval_query += (
        " vegetarian veg menu "
        "veg curries "
        "dal fry "
        "dal makhani "
        "nizami handi "
        "kadai paneer "
        "paneer butter masala"
    )

    if "chicken" in retrieval_query:
        retrieval_query += " chicken menu chicken biryani chicken wings"

    if "paneer" in retrieval_query:
        retrieval_query += " paneer tikka paneer butter masala"

    if "wifi" in retrieval_query:
        retrieval_query += " wifi internet"

    if "parking" in retrieval_query:
        retrieval_query += " parking car parking"

    if "payment" in retrieval_query:
        retrieval_query += " payment online payment card cash upi"

    if "offer" in retrieval_query or "discount" in retrieval_query:
        retrieval_query += " offers discounts"

    if "pet" in retrieval_query:
        retrieval_query += " pets pet policy"

    if "outside food" in retrieval_query:
        retrieval_query += " outside food policy"

    if "email" in retrieval_query:
        retrieval_query += " email contact"

    if "phone" in retrieval_query or "contact" in retrieval_query:
        retrieval_query += " phone mobile contact"
    # ==========================================
    # Hybrid Retrieval (Website + PDF)
    # ==========================================

    # PDF Vector Search
    if pdf_retriever:
     docs = pdf_retriever.invoke(retrieval_query)
     print(f"📄 PDF Vector Results: {len(docs)}")
     all_docs.extend(docs)

    # PDF BM25 Search
    if pdf_keyword_retriever:
     docs = pdf_keyword_retriever.invoke(retrieval_query)
     print(f"📑 PDF BM25 Results: {len(docs)}")
     all_docs.extend(docs)

    # Website Vector Search
    if website_retriever:
     docs = website_retriever.invoke(retrieval_query)
     print(f"🌐 Website Vector Results: {len(docs)}")
     all_docs.extend(docs)

    # Website BM25 Search
    if website_keyword_retriever:
     docs = website_keyword_retriever.invoke(retrieval_query)
     print(f"🔑 Website BM25 Results: {len(docs)}")
     all_docs.extend(docs)

    if not all_docs:
      return {
        "answer": "I'm designed to answer questions only from the loaded website or uploaded PDF.",
        "sources": [],
        "confidence": "Low",
    }

    # ==========================================
    # Detect Menu Question (Only for Source Display)
    #  ==========================================

    menu_question = any(
    word in question.lower()
    for word in [
        "menu",
        "price",
        "cost",
        "veg",
        "biryani",
        "dessert",
        "drink",
        "drinks",
        "beverage",
        "beverages",
        "juice",
        "lassi",
        "falooda",
        "starter",
        "bread",
        "roti",
        "naan",
        "paratha",
        "curry",
        "paneer",
        "chicken",
        "mutton",
        "egg",
    ]
)
    
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

    # Keep fewer website chunks and more menu chunks
    website_context = website_context[:10]
    pdf_context = pdf_context[:10]

    context = f"""
================ WEBSITE KNOWLEDGE ================

{chr(10).join(website_context)}

================ PDF KNOWLEDGE ================

{chr(10).join(pdf_context)}

==================================================

IMPORTANT:

- Use BOTH Website Knowledge and PDF Knowledge.
- If the answer exists in both, combine them.
- Never ignore the PDF.
- Never ignore the Website.
- If menu information exists in the PDF, always use it.
- If restaurant information exists on the Website, use it.
"""
    # ==========================================
    # Build Conversation Memory
    # ==========================================

    conversation_context = ""

    if conversation_history:
        conversation_context += "\n========== PREVIOUS CONVERSATION =========="
        conversation_context += "\n\n"

        for chat in conversation_history:
            conversation_context += (
                f"\nUser: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n"
            )

        conversation_context += "\n===========================================\n"

    # ==========================================
    # Generate Answer
    # ==========================================
    answer = generate_answer(
        provider=provider,
        context=context,
        question=question,
        conversation_history=conversation_context,
    )

    # ==========================================
    # Out-of-Domain Detection
    # ==========================================
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
    # Source Attribution (Relevant Sources Only)
    # ==========================================

    sources = []
    added = set()


    for doc in unique_docs:
        metadata = doc.metadata
        source = metadata.get("source", "")

        if source.startswith("http"):

           key = ("Website", "Website")

           if key not in added:
               added.add(key)
               sources.append({
                   "type": "Website",
                   "url": source
                })

        else:

           filename = Path(source).name if source else "Unknown PDF"
           page = metadata.get("page")

           key = ("PDF", filename)

           if key not in added:
               added.add(key)
               sources.append({
                   "type": "PDF",
                   "file": filename,
                   "page": page + 1 if page is not None else None
                })

    # ==========================================
    # Confidence Score
    # ==========================================

    retrieved_docs = len(unique_docs)
    relevant_sources = len(sources)

    if relevant_sources == 0:
        confidence = "Low"
    elif relevant_sources >= 2 and retrieved_docs >= 4:
        confidence = "High"
    elif relevant_sources >= 1:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }
