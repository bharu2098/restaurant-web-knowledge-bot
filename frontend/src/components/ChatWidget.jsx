import { useEffect, useRef } from "react";

import ChatMessage from "./ChatMessage";
import SuggestedQuestions from "./SuggestedQuestions";
import LoadingSpinner from "./LoadingSpinner";

function ChatWidget({ messages, loading = false }) {
  const messagesEndRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="flex-1 bg-white rounded-2xl border border-gray-200 shadow-md overflow-hidden">

      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4">
        <h2 className="text-lg font-semibold text-gray-800">
          AI Assistant
        </h2>

        <p className="text-sm text-gray-500">
          Ask anything about your restaurant documents or website.
        </p>
      </div>

      {/* Messages */}
      <div className="h-[500px] overflow-y-auto p-6 bg-gray-50">

        {messages.length === 0 && !loading ? (
          <SuggestedQuestions />
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message}
              />
            ))}

            {loading && <LoadingSpinner />}

            {/* Auto-scroll target */}
            <div ref={messagesEndRef}></div>
          </>
        )}

      </div>

    </div>
  );
}

export default ChatWidget;