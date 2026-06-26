from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path: str):
    """
    Load a PDF file and return LangChain documents.
    """

    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        print(f"✅ Loaded {len(documents)} pages from PDF")

        return documents

    except Exception as e:
        print(f"❌ Error loading PDF: {e}")
        raise