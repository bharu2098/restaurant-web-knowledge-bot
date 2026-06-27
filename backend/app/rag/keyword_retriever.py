from langchain_community.retrievers import BM25Retriever


def create_keyword_retriever(chunks):
    """
    Create a BM25 keyword retriever from document chunks.
    """

    retriever = BM25Retriever.from_documents(chunks)

    retriever.k = 2

    print("✅ BM25 Keyword Retriever Created Successfully")

    return retriever