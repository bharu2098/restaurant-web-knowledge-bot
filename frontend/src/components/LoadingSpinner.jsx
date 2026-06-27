import { Bot, Loader2 } from "lucide-react";

function LoadingSpinner() {
  return (
    <div className="flex items-start gap-3 py-6">

      {/* AI Avatar */}
      <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
        <Bot className="text-blue-600" size={20} />
      </div>

      {/* Loading Bubble */}
      <div className="bg-white border border-gray-200 rounded-2xl px-5 py-4 shadow-sm">

        <div className="flex items-center gap-2 mb-2">

          <Loader2
            size={18}
            className="animate-spin text-blue-600"
          />

          <span className="font-semibold text-gray-700">
            Restaurant AI is thinking...
          </span>

        </div>

        <div className="flex gap-2 mt-3">

          <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></span>

          <span
            className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
            style={{ animationDelay: "0.2s" }}
          ></span>

          <span
            className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
            style={{ animationDelay: "0.4s" }}
          ></span>

        </div>

      </div>

    </div>
  );
}

export default LoadingSpinner;