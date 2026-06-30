from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import GOOGLE_API_KEY


def get_embedding_model(provider="gemini"):

    print(f"Embedding Provider: {provider}")

    if provider == "gemini":
        print(">>> Using Gemini Embeddings")
        return GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )

    elif provider == "groq":
        print(">>> Using HuggingFace Embeddings")
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")