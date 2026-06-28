import { useState, useRef, useEffect } from "react";
import {
  X,
  Bot,
  User,
  SendHorizontal,
  Loader2,
} from "lucide-react";

import { sendMessage } from "../services/api";

const welcomeMessage = {
  role: "assistant",
  content:
    "👋 Welcome to Xotic Restaurant!\n\nI'm your AI Restaurant Assistant.\n\nYou can ask me about:\n\n🍕 Menu\n💰 Prices\n📍 Address\n📞 Contact Number\n🕒 Opening Hours\n🥗 Ingredients\n🔥 Special Offers",
};

function CustomerChat({ open, onClose }) {
  const [messages, setMessages] = useState([welcomeMessage]);

  const [text, setText] = useState("");

  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // =====================================
  // Reset Chat Every Time Chat Opens
  // =====================================

  useEffect(() => {
    if (open) {
      setMessages([welcomeMessage]);
      setText("");
      setLoading(false);
    }
  }, [open]);

  // =====================================
  // Auto Scroll
  // =====================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  if (!open) return null;

  // =====================================
  // Send Message
  // =====================================

  const send = async () => {
    if (!text.trim() || loading) return;

    const question = text.trim();

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
      const response = await sendMessage(
        question,
        "groq"
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            response.answer ||
            response.response ||
            "Sorry, I couldn't find that information.",

          sources: response.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "❌ Unable to connect to the restaurant server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // =====================================
  // Enter Key
  // =====================================

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  // =====================================
  // Close Chat
  // =====================================

  const handleClose = () => {
    onClose();
  };
      return (
    <div className="fixed bottom-24 right-6 w-[370px] h-[560px] bg-white rounded-3xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden z-50 animate-in slide-in-from-bottom-5 duration-300">

      {/* ================= Header ================= */}

      <div className="bg-orange-500 text-white px-5 py-4 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="w-11 h-11 rounded-full bg-white/20 flex items-center justify-center">

            <Bot size={22} />

          </div>

          <div>

            <h2 className="font-bold text-lg">
              Restaurant AI
            </h2>

            <p className="text-xs opacity-90">
              🟢 Online • Ready to Help
            </p>

          </div>

        </div>

        <button
          onClick={handleClose}
          className="w-9 h-9 rounded-full hover:bg-orange-600 transition flex items-center justify-center"
        >
          <X size={22} />
        </button>

      </div>

      {/* ================= Messages ================= */}

      <div className="flex-1 overflow-y-auto bg-gray-100 px-4 py-5">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`flex mb-5 ${
              msg.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            {/* Assistant Avatar */}

            {msg.role === "assistant" && (

              <div className="mr-2">

                <div className="w-9 h-9 rounded-full bg-orange-500 text-white flex items-center justify-center">

                  <Bot size={18} />

                </div>

              </div>

            )}

            {/* Message Bubble */}

            <div
              className={`max-w-[78%] rounded-2xl px-4 py-3 shadow-sm ${
                msg.role === "user"
                  ? "bg-orange-500 text-white rounded-br-md"
                  : "bg-white border rounded-bl-md"
              }`}
            >

              <p className="text-sm whitespace-pre-wrap leading-6">
                {msg.content}
              </p>

              {/* Sources */}

              {msg.sources &&
                msg.sources.length > 0 && (

                  <div className="mt-3 pt-2 border-t border-gray-200">

                    <p className="text-xs font-semibold text-gray-500 mb-2">
                      Sources
                    </p>

                    <div className="flex flex-wrap gap-2">

                      {msg.sources.map((source, i) => (

                        <span
                          key={i}
                          className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full"
                        >
                          {source.type === "Website"
                            ? "🌐 Website"
                            : `📄 ${source.file}`}
                        </span>

                      ))}

                    </div>

                  </div>

                )}

            </div>

            {/* User Avatar */}

            {msg.role === "user" && (

              <div className="ml-2">

                <div className="w-9 h-9 rounded-full bg-blue-500 text-white flex items-center justify-center">

                  <User size={18} />

                </div>

              </div>

            )}

          </div>

        ))}

        {/* Typing Indicator */}

        {loading && (

          <div className="flex items-center gap-3 text-gray-600">

            <Loader2
              size={18}
              className="animate-spin"
            />

            <span className="text-sm">
              Restaurant AI is typing...
            </span>

          </div>

        )}

        <div ref={messagesEndRef} />

      </div>
             {/* ================= Input ================= */}

      <div className="border-t bg-white p-4">

        <div className="flex gap-2">

          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about menu, prices..."
            disabled={loading}
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-orange-500 disabled:bg-gray-100"
          />

          <button
            onClick={send}
            disabled={!text.trim() || loading}
            className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all ${
              loading || !text.trim()
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-orange-500 hover:bg-orange-600 text-white"
            }`}
          >
            {loading ? (
              <Loader2
                size={18}
                className="animate-spin"
              />
            ) : (
              <SendHorizontal size={20} />
            )}
          </button>

        </div>

        <p className="text-[11px] text-center text-gray-400 mt-3">
          Powered by Restaurant AI • Website + PDF Knowledge
        </p>

      </div>

    </div>
  );
}

export default CustomerChat;