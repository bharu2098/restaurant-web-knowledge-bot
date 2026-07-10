from langchain_chroma import Chroma
from app.rag.embeddings import get_embedding_model


def create_vector_store(
    chunks,
    persist_directory: str,
    collection_name: str,
    provider: str = "gemini",
):

    embeddings = get_embedding_model(provider)

    # Debug logs
    print("=" * 80)
    print("Embedding object:", type(embeddings))
    print("Chunks:", len(chunks))
    print("First chunk length:", len(chunks[0].page_content))
    print("=" * 80)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )

    print(f"✅ Stored {len(chunks)} chunks in {persist_directory}")

    return vector_store