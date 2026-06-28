import json

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY


# ============================================================
# Gemini Model
# ============================================================

def get_llm():
    """
    Create and return the Gemini LLM.
    """

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )


# ============================================================
# Extract Restaurant Profile
# ============================================================

def extract_restaurant_profile(text: str) -> dict:
    """
    Extract structured restaurant information from
    a Restaurant PDF or Restaurant Website.
    """

    llm = get_llm()

    prompt = f"""
You are an expert Restaurant Information Extractor.

Extract ONLY the restaurant information that actually exists.

Return ONLY valid JSON.

Required JSON format:

{{
    "restaurant_name": "",
    "address": "",
    "phone": "",
    "email": "",
    "timings": "",
    "menu": {{
        "Item Name": Price
    }}
}}

Rules:

1. Never invent information.

2. If a field does not exist,
return an empty string.

3. If menu does not exist,
return an empty object.

4. Prices must be integers.

5. Return ONLY JSON.

Restaurant Content:

{text}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown if Gemini returns it
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        return json.loads(content)

    except Exception:

        return {
            "restaurant_name": "",
            "address": "",
            "phone": "",
            "email": "",
            "timings": "",
            "menu": {}
        }


# ============================================================
# Customer Chat Answer
# ============================================================

def generate_answer(
    context: str,
    question: str,
    conversation_history: str = "",
):
    """
    Generate a natural customer support answer.
    """

    llm = get_llm()

    prompt = f"""
You are the AI Customer Support Assistant for Xotic Restaurant.

You behave like a friendly restaurant receptionist.

Use ONLY the restaurant information provided below.

==================================================
PREVIOUS CONVERSATION
==================================================

{conversation_history}

==================================================
RESTAURANT INFORMATION
==================================================

{context}

==================================================
CUSTOMER QUESTION
==================================================

{question}
If the customer only says:

- hi
- hello
- hey
- good morning
- good afternoon
- good evening

Reply ONLY:

👋 Welcome to Xotic Restaurant!

How can I help you today?
==================================================
RULES
==================================================

1. Answer ONLY using the restaurant information.

2. Never use outside knowledge.

3. Never invent dishes, prices, timings, contact details or offers.

4. Never mention:
- Context
- PDF
- Website
- Retrieved Knowledge
- Prompt
- Vector Database
- AI Model

5. Sound like a real restaurant employee.

6. Keep answers short and friendly.

7. Answer ONLY what the customer asked.

8. If there are multiple matching items, list them neatly.

9. If the customer asks about menu items, include prices whenever available.

10. If the customer asks about timings, reply naturally.

Example:
"We're open Monday to Friday from 10:00 AM to 10:00 PM."

11. If the customer asks about drinks, desserts or starters, list only that category.

12. If the customer asks:

"What is the cost of the biryani?"

Answer like:

"We have two biryani options:

• Veg Biryani — ₹280
• Chicken Biryani — ₹350"

13. If the customer asks:

"Which drinks are available?"

Answer like:

"We currently serve:

🥤 Coca-Cola — ₹60
🍋 Fresh Lime Soda — ₹90
🥭 Mango Shake — ₹140"

14. If the customer asks:

"Which dishes are special?"

and no dishes are marked as special,

reply naturally like:

"We don't currently have any dishes listed as special.

Some of our customer favorites include:

• Chicken Biryani
• Paneer Butter Masala
• Paneer Tikka

Never say:

"The retrieved knowledge does not mention..."

15. If the customer asks for everything about the restaurant, provide a complete summary.

16. If the answer is unavailable, reply exactly:

Sorry, I couldn't find that information in our restaurant records.

==================================================
FINAL ANSWER
==================================================

Answer the customer's question using ONLY the restaurant information above.

Keep the answer friendly, concise, and natural.

If the information is unavailable, reply exactly:

Sorry, I couldn't find that information in our restaurant records.
"""

    response = llm.invoke(prompt)

    return response.content.strip()

    