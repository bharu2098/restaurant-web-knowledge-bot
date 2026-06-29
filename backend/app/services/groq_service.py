import json

from groq import Groq

from app.config import GROQ_API_KEY


# ============================================================
# Groq Client
# ============================================================

def get_client():
    """
    Create and return the Groq client.
    """

    return Groq(api_key=GROQ_API_KEY)


# ============================================================
# Extract Restaurant Profile
# ============================================================

def extract_restaurant_profile(text: str) -> dict:
    """
    Extract structured restaurant information
    from a Restaurant Website or Menu PDF.
    """

    client = get_client()

    prompt = f"""
You are an expert Restaurant Information Extractor.

Your task is to extract structured restaurant information from
a restaurant WEBSITE or MENU PDF.

Return ONLY valid JSON.

JSON format:

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

1. restaurant_name must ONLY contain the restaurant name.

Correct Examples:
- Paradise
- Barbeque Nation
- Xotic Restaurant

Wrong Examples:
- Best Biryani Restaurants in Hyderabad | Paradise Food Court
- Privacy Policy
- Home
- Careers
- Contact Us

2. Ignore:
- Navigation menu
- Header
- Footer
- Blogs
- Careers
- Copyright
- GST Numbers
- SEO titles
- Advertisements
- Offers
- Terms & Conditions
- Privacy Policy
3. Menu items must be actual food or beverages.

4. Every menu item must have exactly one numeric price.

Correct:
"Chicken Biryani": 335

Wrong:
"Chicken Biryani": "Chicken cooked with spices"

Wrong:
"Description": "Chicken cooked with spices"

5. Never include food descriptions.

6. Never include ingredients.

7. Never include serving information.

8. Never include duplicate keys.

9. If information does not exist return "".
10. If menu is unavailable return {{}}.

11. Return ONLY valid JSON.
Restaurant Content:

{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content.strip()

    print("\n========== GROQ RAW RESPONSE ==========")
    print(content)
    print("=======================================\n")
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        return json.loads(content)

    except Exception as e:
        print("\n========== JSON ERROR ==========")
        print(e)
        print(content)
        print("================================\n")
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
    Generate a restaurant customer support answer using Groq.
    """

    client = get_client()

    prompt = f"""
You are an AI Customer Support Assistant.

You behave like a friendly restaurant receptionist.

Always answer based on the loaded restaurant.

Use the restaurant name found in the provided information.

Never assume the restaurant is Xotic Restaurant.

Use ONLY the restaurant information below.

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

👋 Welcome to our restaurant!

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
- AI Model
- Vector Database

5. Speak like a restaurant employee.

6. Keep answers short and friendly.

7. Answer only what the customer asked.

8. Do not dump the entire menu unless requested.

9. If multiple menu items match, list only those items.

10. Include prices whenever available.

11. If the customer asks for drinks, desserts, starters or biryani,
return only that category.
12. When BOTH Website and PDF are available:

• Use the Website for:
  - Restaurant overview
  - About Us
  - History
  - Contact details
  - Address
  - Timings
  - Policies
  - FAQs

• Use the PDF for:
  - Menu
  - Prices
  - Drinks
  - Desserts
  - Starters
  - Combos
  - Food categories

• If the customer's question requires information from both, combine both naturally.

• Never ignore either source.
13. Never combine information from different restaurants.

If restaurant information belongs to different restaurants,
reply exactly:

The uploaded menu does not belong to the loaded restaurant. Please upload the correct menu PDF.
14. If the customer's question contains multiple parts, answer ALL parts.

Example:

Question:
"What is a restaurant and what biryanis does Paradise serve?"

Answer:

A restaurant is a business that prepares and serves food and beverages.

Paradise serves:

• Chicken Biryani — ₹335
• Mutton Biryani — ₹369
• Veg Biryani — ₹224
• Egg Biryani — ₹224
15. If the customer asks for restaurant history,
answer only if it exists.

16. If the answer is unavailable reply exactly:

Sorry, I couldn't find that information in our restaurant records.

==================================================
FINAL ANSWER
==================================================

Answer naturally like a restaurant employee.

Always check BOTH Website Knowledge and PDF Knowledge before answering.

If information exists in both, combine it naturally.

If menu information exists in the PDF, prefer the PDF.

If restaurant information exists on the Website, use the Website.

If the question asks for restaurant information and menu information together, answer both.

Never invent information.

Never mix different restaurants.

If the answer cannot be found anywhere, reply exactly:

Sorry, I couldn't find that information in our restaurant records.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Restaurant Customer Support Assistant. "
                    "Answer ONLY using the provided restaurant information. "
                    "Never invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
       
    )

    return response.choices[0].message.content.strip()