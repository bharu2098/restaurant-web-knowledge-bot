import csv
from pathlib import Path

# In-memory chat history
chat_history = []


def save_chat(question: str, answer: str):
    """
    Save a conversation to chat history.
    """

    chat_history.append({
        "question": question,
        "answer": answer
    })


def get_chat_history():
    """
    Return all chat history.
    """

    return chat_history


def clear_chat_history():
    """
    Clear all stored chat history.
    """

    chat_history.clear()


def export_chat_history():
    """
    Export chat history to CSV.
    """

    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)

    csv_file = export_dir / "chat_history.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Question",
            "Answer"
        ])

        for chat in chat_history:

            writer.writerow([
                chat["question"],
                chat["answer"]
            ])

    return csv_file