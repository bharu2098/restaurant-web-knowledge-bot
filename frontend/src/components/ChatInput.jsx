import { useState } from "react";
import { SendHorizontal } from "lucide-react";

import { sendMessage } from "../services/api";

function ChatInput({
  messages,
  setMessages,
  setLoading,
}) {
  const [text, setText] = useState("");

  const send = async () => {
    if (!text.trim()) return;

    const question = text.trim();

    // Show user message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    setText("");
    setLoading(true);

    try {
      const response = await sendMessage(question, "groq");
      console.log("Chat Response:", response);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            response.answer ||
            response.response ||
            "No response received.",

          sources: response.sources || [],

          confidence: response.confidence || "Low",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error.message ||
            "❌ Failed to contact the AI assistant.",

          sources: [],

          confidence: "Low",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="bg-white border-t border-gray-200 p-4">

      <div className="flex gap-3 items-end">

        <textarea
          rows={1}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about your restaurant..."
          className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={send}
          disabled={!text.trim()}
          className={`h-12 w-12 rounded-xl flex items-center justify-center transition ${
            text.trim()
              ? "bg-blue-600 hover:bg-blue-700 text-white"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          <SendHorizontal size={20} />
        </button>

      </div>

      <p className="mt-2 text-xs text-gray-500">
        Press <strong>Enter</strong> to send •{" "}
        <strong>Shift + Enter</strong> for a new line
      </p>

    </div>
  );
}

export default ChatInput;