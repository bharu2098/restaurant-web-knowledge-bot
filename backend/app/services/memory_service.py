"""
Temporary in-memory storage for the Restaurant Knowledge Bot.

Stores:

1. Website Vector Retriever
2. Website BM25 Retriever
3. PDF Vector Retriever
4. PDF BM25 Retriever
5. Restaurant Names
6. Restaurant Profiles
7. Raw Website Text
8. Raw PDF Text
9. Verification Status
10. Latest Uploaded PDF

This can later be replaced with Redis,
a database, or session-based storage.
"""

from typing import Any

# ============================================================
# Website Retrievers
# ============================================================

website_retriever: Any = None
website_keyword_retriever: Any = None

# ============================================================
# PDF Retrievers
# ============================================================

pdf_retriever: Any = None
pdf_keyword_retriever: Any = None

# ============================================================
# Restaurant Names
# ============================================================

pdf_restaurant_name: str | None = None
website_restaurant_name: str | None = None

# ============================================================
# Raw Extracted Text
# ============================================================

pdf_text: str = ""
website_text: str = ""

# ============================================================
# Structured Restaurant Profiles
# ============================================================

pdf_profile: dict = {}
website_profile: dict = {}

# ============================================================
# Verification
# ============================================================

restaurant_verified: bool = False

# ============================================================
# Latest Uploaded PDF
# ============================================================

latest_pdf_filename: str | None = None


# ============================================================
# Website Vector Retriever
# ============================================================

def set_website_retriever(new_retriever: Any):
    global website_retriever
    website_retriever = new_retriever


def get_website_retriever():
    return website_retriever


def clear_website_retriever():
    global website_retriever
    website_retriever = None


# ============================================================
# Website BM25 Retriever
# ============================================================

def set_website_keyword_retriever(new_retriever: Any):
    global website_keyword_retriever
    website_keyword_retriever = new_retriever


def get_website_keyword_retriever():
    return website_keyword_retriever


def clear_website_keyword_retriever():
    global website_keyword_retriever
    website_keyword_retriever = None


# ============================================================
# PDF Vector Retriever
# ============================================================

def set_pdf_retriever(new_retriever: Any):
    global pdf_retriever
    pdf_retriever = new_retriever


def get_pdf_retriever():
    return pdf_retriever


def clear_pdf_retriever():
    global pdf_retriever
    pdf_retriever = None


# ============================================================
# PDF BM25 Retriever
# ============================================================

def set_pdf_keyword_retriever(new_retriever: Any):
    global pdf_keyword_retriever
    pdf_keyword_retriever = new_retriever


def get_pdf_keyword_retriever():
    return pdf_keyword_retriever


def clear_pdf_keyword_retriever():
    global pdf_keyword_retriever
    pdf_keyword_retriever = None


# ============================================================
# PDF Restaurant Name
# ============================================================

def set_pdf_restaurant_name(name: str):
    global pdf_restaurant_name
    pdf_restaurant_name = name.strip()


def get_pdf_restaurant_name():
    return pdf_restaurant_name


# ============================================================
# Website Restaurant Name
# ============================================================

def set_website_restaurant_name(name: str):
    global website_restaurant_name
    website_restaurant_name = name.strip()


def get_website_restaurant_name():
    return website_restaurant_name


# ============================================================
# Raw PDF Text
# ============================================================

def set_pdf_text(text: str):
    global pdf_text
    pdf_text = text


def get_pdf_text():
    return pdf_text


# ============================================================
# Raw Website Text
# ============================================================

def set_website_text(text: str):
    global website_text
    website_text = text


def get_website_text():
    return website_text


# ============================================================
# PDF Restaurant Profile
# ============================================================

def set_pdf_profile(profile: dict):
    global pdf_profile
    pdf_profile = profile


def get_pdf_profile():
    return pdf_profile


# ============================================================
# Website Restaurant Profile
# ============================================================

def set_website_profile(profile: dict):
    global website_profile
    website_profile = profile


def get_website_profile():
    return website_profile


# ============================================================
# Restaurant Verification
# ============================================================

def set_restaurant_verified(status: bool):
    global restaurant_verified
    restaurant_verified = status


def is_restaurant_verified():
    return restaurant_verified


# ============================================================
# Latest Uploaded PDF
# ============================================================

def set_latest_pdf(filename: str):
    global latest_pdf_filename
    latest_pdf_filename = filename


def get_latest_pdf():
    return latest_pdf_filename


# ============================================================
# Clear Restaurant Information
# ============================================================

def clear_restaurant_information():
    global pdf_restaurant_name
    global website_restaurant_name
    global pdf_text
    global website_text
    global pdf_profile
    global website_profile
    global restaurant_verified
    global latest_pdf_filename

    pdf_restaurant_name = None
    website_restaurant_name = None

    pdf_text = ""
    website_text = ""

    pdf_profile = {}
    website_profile = {}

    restaurant_verified = False
    latest_pdf_filename = None


# ============================================================
# Clear Everything
# ============================================================

def clear_all_retrievers():
    global website_retriever
    global website_keyword_retriever
    global pdf_retriever
    global pdf_keyword_retriever

    website_retriever = None
    website_keyword_retriever = None

    pdf_retriever = None
    pdf_keyword_retriever = None

    clear_restaurant_information()