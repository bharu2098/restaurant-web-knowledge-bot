"""
LLM Service

Routes all LLM requests to the selected provider.

Supported Providers
-------------------
- gemini
- groq
"""

from app.services.gemini_service import (
    generate_answer as gemini_generate,
    extract_restaurant_profile as gemini_extract,
)

from app.services.groq_service import (
    generate_answer as groq_generate,
    extract_restaurant_profile as groq_extract,
)


# ==========================================================
# Supported Providers
# ==========================================================

SUPPORTED_PROVIDERS = {
    "gemini",
    "groq",
}


# ==========================================================
# Validate Provider
# ==========================================================

def validate_provider(provider: str) -> str:
    """
    Validate and normalize the provider name.
    """

    provider = provider.strip().lower()

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported provider '{provider}'. "
            f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
        )

    return provider


# ==========================================================
# Generate Chat Answer
# ==========================================================

def generate_answer(
    provider: str,
    context: str,
    question: str,
    conversation_history: str = "",
):
    """
    Generate a customer response using the selected LLM.

    Parameters
    ----------
    provider : str
        gemini or groq

    context : str
        Combined Website + PDF knowledge.

    question : str
        User question.

    conversation_history : str
        Previous conversation.
    """

    provider = validate_provider(provider)

    if provider == "gemini":
        return gemini_generate(
            context=context,
            question=question,
            conversation_history=conversation_history,
        )

    elif provider == "groq":
        return groq_generate(
            context=context,
            question=question,
            conversation_history=conversation_history,
        )


# ==========================================================
# Extract Restaurant Profile
# ==========================================================

def extract_restaurant_profile(
    text: str,
    provider: str = "gemini",
):
    """
    Extract structured restaurant information
    from website or PDF.
    """

    provider = validate_provider(provider)

    if provider == "gemini":
        return gemini_extract(text)

    elif provider == "groq":
        return groq_extract(text)