from rag.rag_pipeline import ask_website

url = "https://example.com"

question = "What is this website about?"

answer = ask_website(url, question)

print("\nAnswer:\n")
print(answer)