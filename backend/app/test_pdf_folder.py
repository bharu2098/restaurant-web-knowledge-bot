from app.rag.pdf_loader import load_pdf

pdf_path = "sample_data/sample_menu.pdf"

documents = load_pdf(pdf_path)

print("\nTotal Pages:", len(documents))
print("=" * 60)

if documents:
    print(documents[0].page_content[:500])