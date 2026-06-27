"""
Temporary in-memory storage for retrievers.

Stores separate retrievers for:

1. Website Vector Retriever
2. Website Keyword Retriever (BM25)
3. PDF Vector Retriever
4. PDF Keyword Retriever (BM25)

Later this can be replaced with Redis,
a database, or session-based storage.
"""

from typing import Any


# =====================================
# Website Retrievers
# =====================================

website_retriever: Any = None
website_keyword_retriever: Any = None


# =====================================
# PDF Retrievers
# =====================================

pdf_retriever: Any = None
pdf_keyword_retriever: Any = None


# ============================================================
# Website Vector Retriever
# ============================================================

def set_website_retriever(new_retriever: Any) -> None:
    global website_retriever
    website_retriever = new_retriever


def get_website_retriever() -> Any:
    return website_retriever


def clear_website_retriever() -> None:
    global website_retriever
    website_retriever = None


# ============================================================
# Website Keyword Retriever (BM25)
# ============================================================

def set_website_keyword_retriever(new_retriever: Any) -> None:
    global website_keyword_retriever
    website_keyword_retriever = new_retriever


def get_website_keyword_retriever() -> Any:
    return website_keyword_retriever


def clear_website_keyword_retriever() -> None:
    global website_keyword_retriever
    website_keyword_retriever = None


# ============================================================
# PDF Vector Retriever
# ============================================================

def set_pdf_retriever(new_retriever: Any) -> None:
    global pdf_retriever
    pdf_retriever = new_retriever


def get_pdf_retriever() -> Any:
    return pdf_retriever


def clear_pdf_retriever() -> None:
    global pdf_retriever
    pdf_retriever = None


# ============================================================
# PDF Keyword Retriever (BM25)
# ============================================================

def set_pdf_keyword_retriever(new_retriever: Any) -> None:
    global pdf_keyword_retriever
    pdf_keyword_retriever = new_retriever


def get_pdf_keyword_retriever() -> Any:
    return pdf_keyword_retriever


def clear_pdf_keyword_retriever() -> None:
    global pdf_keyword_retriever
    pdf_keyword_retriever = None


# ============================================================
# Clear Everything
# ============================================================

def clear_all_retrievers() -> None:
    global website_retriever, website_keyword_retriever
    global pdf_retriever, pdf_keyword_retriever

    website_retriever = None
    website_keyword_retriever = None
    pdf_retriever = None
    pdf_keyword_retriever = None