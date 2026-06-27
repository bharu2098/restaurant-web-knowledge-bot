import csv
from pathlib import Path

# ==========================================
# In-Memory Chat History
# ==========================================

chat_history = []


# ==========================================
# Save Chat
# ==========================================

def save_chat(question: str, answer: str):
    """
    Save a conversation to chat history.
    """

    chat_history.append({
        "question": question,
        "answer": answer
    })


# ==========================================
# Get Full Chat History
# ==========================================

def get_chat_history():
    """
    Return all stored conversations.
    """

    return chat_history


# ==========================================
# Get Recent Conversation Memory
# ==========================================

def get_recent_chat_history(limit: int = 5):
    """
    Return the last N conversations.

    This is used as conversation memory so the
    assistant understands follow-up questions.
    """

    if limit <= 0:
        return []

    return chat_history[-limit:]


# ==========================================
# Clear Chat History
# ==========================================

def clear_chat_history():
    """
    Remove all stored conversations.
    """

    chat_history.clear()


# ==========================================
# Export Chat History
# ==========================================

def export_chat_history():
    """
    Export chat history as a CSV file.
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