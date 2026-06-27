import { User, Bot } from "lucide-react";
import SourceBadge from "./SourceBadge";

function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex gap-3 mb-6 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {/* AI Avatar */}
      {!isUser && (
        <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
          <Bot className="text-blue-600" size={20} />
        </div>
      )}

      {/* Message Bubble */}
      <div
        className={`max-w-[75%] rounded-2xl px-5 py-4 shadow-sm ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white border border-gray-200 text-gray-800"
        }`}
      >
        <p className="font-semibold mb-2">
          {isUser ? "You" : "Restaurant AI"}
        </p>

        <p className="whitespace-pre-wrap leading-7">
          {message.content}
        </p>

        {/* Sources */}
        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {message.sources.map((source, index) => (
                <SourceBadge
                  key={index}
                  source={source}
                />
              ))}
            </div>
          )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
          <User className="text-green-600" size={20} />
        </div>
      )}
    </div>
  );
}

export default ChatMessage;