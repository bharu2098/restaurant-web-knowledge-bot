from app.services.gemini_service import (
    generate_answer as gemini_generate,
    extract_restaurant_profile as gemini_extract,
)

from app.services.groq_service import (
    generate_answer as groq_generate,
    extract_restaurant_profile as groq_extract,
)


# ============================================================
# Chat Answer
# ============================================================

def generate_answer(
    provider: str,
    context: str,
    question: str,
    conversation_history: str = "",
):
    """
    Route the request to the selected LLM provider.
    """

    provider = provider.strip().lower()

    if provider == "gemini":
        return gemini_generate(
            context=context,
            question=question,
            conversation_history=conversation_history,
        )

    if provider == "groq":
        return groq_generate(
            context=context,
            question=question,
            conversation_history=conversation_history,
        )

    raise ValueError(
        f"Unsupported provider: {provider}"
    )


# ============================================================
# Restaurant Profile Extraction
# ============================================================

def extract_restaurant_profile(
    text: str,
    provider: str = "gemini",
):
    """
    Extract restaurant information using the selected LLM.
    """

    provider = provider.strip().lower()

    if provider == "gemini":
        return gemini_extract(text)

    if provider == "groq":
        return groq_extract(text)

    raise ValueError(
        f"Unsupported provider: {provider}"
    )