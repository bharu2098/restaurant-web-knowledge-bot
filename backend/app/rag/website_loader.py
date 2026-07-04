import os

# -------------------------------------------------------
# Set User-Agent BEFORE importing WebBaseLoader
# -------------------------------------------------------

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from langchain_community.document_loaders import WebBaseLoader


# ==========================================================
# Configuration
# ==========================================================

MAX_PAGES = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


# ==========================================================
# Get Internal Website Links
# ==========================================================

def get_internal_links(base_url: str):
    """
    Crawl homepage and collect internal links.
    """

    print("\n🌐 Crawling Website...")

    response = requests.get(
        base_url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()
    print("\n" + "=" * 80)
    print("REQUEST URL :", response.url)
    print("STATUS CODE :", response.status_code)
    print("FIRST 1000 HTML:\n")
    print(response.text[:1000])
    print("=" * 80)

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    domain = urlparse(base_url).netloc

    links = set()

    links.add(base_url.rstrip("/"))

    for tag in soup.find_all("a", href=True):

        href = tag["href"].strip()

        if not href:
            continue

        full_url = urljoin(base_url, href)

        parsed = urlparse(full_url)

        if parsed.netloc != domain:
            continue

        if parsed.scheme not in ["http", "https"]:
            continue

        if "#" in full_url:
            full_url = full_url.split("#")[0]

        full_url = full_url.rstrip("/")
        # Skip unwanted pages
        if any(word in full_url.lower() for word in [
            "login",
            "signin",
            "signup",
            "cart",
           "checkout",
           "privacy",
           "terms",
           "policy",
           "faq",
     ]):
         continue

        if any(
            full_url.lower().endswith(ext)
            for ext in [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".svg",
                ".css",
                ".js",
                ".ico",
                ".pdf",
                ".zip",
                ".xml",
            ]
        ):
            continue

        links.add(full_url)

    links = list(links)

    print(f"✅ Found {len(links)} internal links")

    return links[:MAX_PAGES]


# ==========================================================
# Load Website
# ==========================================================

def load_website(url: str):
    """
    Crawl a website and load multiple pages.
    """

    try:

        urls = get_internal_links(url)

        print("\n📄 Pages To Load:")

        for page in urls:
            print(page)

        documents = []

        for page in urls:

            try:

                loader = WebBaseLoader(
                    web_paths=(page,),
                    requests_kwargs={
                        "headers": HEADERS,
                        "timeout": 30,
                    },
                )

                docs = loader.load()

                if docs:
                    print("\n" + "=" * 80)
                    print("LOADED URL :", page)
                    print("SOURCE     :", docs[0].metadata.get("source", "Unknown"))
                    print("TITLE      :", docs[0].metadata.get("title", "Unknown"))
                    print("FIRST 1000 CHARACTERS:\n")
                    print(docs[0].page_content[:1000])
                    print("=" * 80)

                documents.extend(docs)

                print(
                    f"✅ Loaded: {page} ({len(docs)} document)"
               )

            except Exception as e:

                print(
                    f"❌ Skipped {page}"
                )

                print(e)

        print("\n" + "=" * 70)

        print(f"📄 Loaded Documents: {len(documents)}")

        total_chars = 0

        for i, doc in enumerate(documents):

            total_chars += len(doc.page_content)

            print(f"\n📄 Document {i+1}")

            print(
                "Source:",
                doc.metadata.get(
                    "source",
                    "Unknown",
                ),
            )

            print(
                "Length:",
                len(doc.page_content),
            )

            print(doc.page_content[:300])

        print("\n📊 Total Characters:", total_chars)

        print("=" * 70)

        return documents

    except Exception as e:

        print(f"\n❌ Error loading website")

        print(e)

        raise