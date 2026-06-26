from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model


def create_vector_store(chunks):
    """
    Create a ChromaDB vector store from document chunks.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB")

    return vector_store