from langchain_core.vectorstores import VectorStoreRetriever


def create_retriever(vector_store):
    """
    Create a semantic vector retriever from ChromaDB.
    """

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    print("✅ Vector Retriever Created Successfully")

    return retriever