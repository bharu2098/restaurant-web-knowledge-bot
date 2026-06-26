from langchain_community.document_loaders import WebBaseLoader


def load_website(url: str):
    """
    Load website content and return documents.
    """

    try:
        loader = WebBaseLoader(url)

        documents = loader.load()

        print("=" * 50)
        print(f"Loaded Documents: {len(documents)}")

        for i, doc in enumerate(documents):
            print(f"\nDocument {i+1}")
            print("Length:", len(doc.page_content))
            print(doc.page_content[:500])

        print("=" * 50)

        return documents

    except Exception as e:
        print("❌ Error loading website:", e)
        raise