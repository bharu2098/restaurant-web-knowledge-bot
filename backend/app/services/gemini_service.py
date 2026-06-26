from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY


def get_llm():
    """
    Create and return the Gemini LLM.
    """

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
    )


def generate_answer(context: str, question: str):
    """
    Generate an answer using the Website and PDF knowledge.
    """

    llm = get_llm()

    prompt = f"""
You are the AI assistant for the Restaurant Web Knowledge Bot.

You have TWO knowledge sources.

1. WEBSITE KNOWLEDGE
2. PDF KNOWLEDGE

Your job is to answer ONLY using the provided knowledge.

=============================
IMPORTANT RULES
=============================

1. Read BOTH Website Knowledge and PDF Knowledge carefully.

2. The user's question may contain MULTIPLE QUESTIONS.

3. Answer EVERY PART of the question separately.

4. If information comes from BOTH Website and PDF,
combine it into ONE complete answer.

5. If one part is found only in Website Knowledge,
answer that part.

6. If another part is found only in PDF Knowledge,
answer that part.

7. Never use outside knowledge.

8. Never guess.

9. Never invent information.

10. ONLY reply with

"I couldn't find that information in the loaded website or uploaded PDF."

IF AND ONLY IF absolutely NO relevant information exists in BOTH Website Knowledge AND PDF Knowledge.

=============================
FORMATTING
=============================

• Use bullet points when appropriate.

• Preserve formatting for:
- Opening hours
- Menu items
- Prices
- Contact information
- Addresses

• Never mention:
Website Knowledge
PDF Knowledge
Context
Prompt

=============================
CONTEXT
=============================

{context}

=============================
USER QUESTION
=============================

{question}

=============================
FINAL ANSWER
=============================

Provide one complete answer using every relevant piece of information from the available knowledge sources.
"""

    response = llm.invoke(prompt)

    return response.content.strip()