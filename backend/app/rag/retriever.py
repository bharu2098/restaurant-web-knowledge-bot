from langchain_core.vectorstores import VectorStoreRetriever


def create_retriever(vector_store):
    """
    Create a retriever from the vector store.
    """

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    print("✅ Retriever Created Successfully")

    return retriever