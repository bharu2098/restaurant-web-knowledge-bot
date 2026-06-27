from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services.chat_service import (
    get_chat_history,
    clear_chat_history,
    export_chat_history,
)

router = APIRouter()


@router.get("/")
async def history():
    """
    Return all chat history.
    """

    return {
        "total_chats": len(get_chat_history()),
        "history": get_chat_history()
    }


@router.delete("/")
async def clear_history():
    """
    Clear all chat history.
    """

    clear_chat_history()

    return {
        "status": "success",
        "message": "Chat history cleared successfully."
    }


@router.get("/export")
async def export_history():
    """
    Export chat history as CSV.
    """

    csv_file = export_chat_history()

    return FileResponse(
        path=csv_file,
        media_type="text/csv",
        filename="chat_history.csv"
    )