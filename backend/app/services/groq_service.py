from groq import Groq

from app.config import GROQ_API_KEY


def generate_answer(context: str, question: str):
    """
    Generate an answer using the Groq LLM.
    """

    client = Groq(
        api_key=GROQ_API_KEY
    )

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

10. If the user's question CANNOT be answered using the Website Knowledge
or PDF Knowledge, reply EXACTLY with:

"I'm designed to answer questions only from the loaded website or uploaded PDF."

11. Never answer using your own knowledge.

12. Never use information that is not present in the provided context.

13. If the retrieved context is unrelated to the user's question,
reply ONLY with:

"I'm designed to answer questions only from the loaded website or uploaded PDF."

=============================
CONTEXT
=============================

{context}

=============================
QUESTION
=============================

{question}

=============================
FINAL ANSWER
=============================
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()