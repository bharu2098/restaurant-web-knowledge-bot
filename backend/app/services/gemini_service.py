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


def generate_answer(
    context: str,
    question: str,
    conversation_history: str = "",
):
    """
    Generate an answer using the retrieved knowledge.
    """

    llm = get_llm()

    prompt = f"""
You are an AI Knowledge Assistant.

Your job is to answer questions ONLY using the retrieved knowledge provided below.

The retrieved knowledge may come from:

• One or more websites
• One or more PDF documents
• Both websites and PDFs together

==================================================
PREVIOUS CONVERSATION
==================================================

{conversation_history}

==================================================
IMPORTANT RULES
==================================================

1. Read the retrieved knowledge carefully before answering.

2. Read the previous conversation before answering.

3. If the current question refers to:

- it
- they
- them
- this
- that
- these
- those
- its
- their

use the previous conversation ONLY to understand what the user is referring to.

4. Answer ONLY using the retrieved knowledge.

5. Never use your own knowledge.

6. Never guess.

7. Never invent information.

8. If information exists in multiple retrieved sources,
combine it into one complete answer.

9. If the user's question contains multiple questions,
answer every part.

10. If the answer cannot be found in the retrieved knowledge,
reply EXACTLY with:

I'm designed to answer questions only from the loaded website or uploaded PDF.

11. Ignore previous conversation whenever it conflicts with the retrieved knowledge.

12. Never mention:

- Website Knowledge
- PDF Knowledge
- Retrieved Knowledge
- Context
- Prompt
- Previous Conversation

==================================================
FORMATTING
==================================================

• Use bullet points whenever appropriate.

• Preserve formatting for:

- Tables
- Prices
- Menu items
- Addresses
- Contact information
- Dates
- Timings
- Lists

==================================================
RETRIEVED KNOWLEDGE
==================================================

{context}

==================================================
CURRENT QUESTION
==================================================

{question}

==================================================
FINAL ANSWER
==================================================

Answer ONLY using the retrieved knowledge.

Use the previous conversation ONLY to resolve follow-up questions such as:

- it
- they
- them
- this
- that
- those
- these

If the answer is not available in the retrieved knowledge, reply exactly:

I'm designed to answer questions only from the loaded website or uploaded PDF.
"""

    response = llm.invoke(prompt)

    return response.content.strip()