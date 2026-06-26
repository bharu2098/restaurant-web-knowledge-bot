"""
Temporary in-memory storage for retrievers.

Stores separate retrievers for:

1. Website Knowledge Base
2. Uploaded PDF Knowledge Base

Later this can be replaced with Redis,
a database, or session-based storage.
"""

from typing import Any

# Website Retriever
website_retriever: Any = None

# PDF Retriever
pdf_retriever: Any = None


# ===========================
# Website Retriever
# ===========================

def set_website_retriever(new_retriever: Any) -> None:
    """
    Store the website retriever.
    """
    global website_retriever
    website_retriever = new_retriever


def get_website_retriever() -> Any:
    """
    Return the website retriever.
    """
    return website_retriever


def clear_website_retriever() -> None:
    """
    Remove the website retriever.
    """
    global website_retriever
    website_retriever = None


# ===========================
# PDF Retriever
# ===========================

def set_pdf_retriever(new_retriever: Any) -> None:
    """
    Store the PDF retriever.
    """
    global pdf_retriever
    pdf_retriever = new_retriever


def get_pdf_retriever() -> Any:
    """
    Return the PDF retriever.
    """
    return pdf_retriever


def clear_pdf_retriever() -> None:
    """
    Remove the PDF retriever.
    """
    global pdf_retriever
    pdf_retriever = None


# ===========================
# Clear Everything
# ===========================

def clear_all_retrievers() -> None:
    """
    Remove both website and PDF retrievers.
    """
    global website_retriever, pdf_retriever

    website_retriever = None
    pdf_retriever = None