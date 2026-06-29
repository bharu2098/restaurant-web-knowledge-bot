from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model


def create_vector_store(
    chunks,
    persist_directory: str,
    collection_name: str,
):
    """
    Create a ChromaDB vector store.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )

    print(
        f"✅ Stored {len(chunks)} chunks in {persist_directory}"
    )

    return vector_store