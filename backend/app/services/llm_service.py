from app.services.gemini_service import generate_answer as gemini_generate
from app.services.groq_service import generate_answer as groq_generate


def generate_answer(
    provider: str,
    context: str,
    question: str,
    conversation_history: str = "",
):
    """
    Route the request to the selected LLM provider.
    """

    provider = provider.lower()

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

    raise ValueError(f"Unsupported LLM provider: {provider}")