import os

# Set User-Agent before importing loader
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)

from langchain_community.document_loaders import WebBaseLoader


def load_website(url: str):
    """
    Load website content and return LangChain documents.
    """

    try:

        loader = WebBaseLoader(
            web_paths=(url,),
            requests_kwargs={
                "headers": {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0.0.0 Safari/537.36"
                    )
                },
                "timeout": 30,
            },
        )

        documents = loader.load()

        print("=" * 60)
        print(f"📄 Loaded Documents: {len(documents)}")

        for i, doc in enumerate(documents):
            print(f"\n📄 Document {i + 1}")
            print("Source:", doc.metadata.get("source", "Unknown"))
            print("Length:", len(doc.page_content))
            print(doc.page_content[:500])

        print("=" * 60)

        return documents

    except Exception as e:
        print(f"❌ Error loading website: {e}")
        raise