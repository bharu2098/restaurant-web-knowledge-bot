from services.gemini_service import generate_answer

context = """
Our restaurant is open from 10 AM to 10 PM.
We serve Pizza, Pasta and Burgers.
"""

question = "What are your opening hours?"

answer = generate_answer(context, question)

print(answer)