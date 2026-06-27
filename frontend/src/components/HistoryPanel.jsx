import { useEffect, useState } from "react";
import {
  History,
  Trash2,
  Download,
  X,
} from "lucide-react";

import {
  getHistory,
  clearHistory,
  exportHistory,
} from "../services/api";

function HistoryPanel({ setShowHistory }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data.history || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleClear = async () => {
    if (!window.confirm("Clear all chat history?")) return;

    try {
      await clearHistory();
      setHistory([]);
    } catch (error) {
      console.error(error);
    }
  };

  const handleExport = () => {
    exportHistory();
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-end z-50">

      <div className="w-full max-w-md bg-white h-full shadow-2xl flex flex-col">

        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b">

          <div className="flex items-center gap-2">

            <History className="text-blue-600" size={22} />

            <h2 className="text-xl font-semibold">
              Chat History
            </h2>

          </div>

          <button onClick={() => setShowHistory(false)}>
            <X />
          </button>

        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-5">

          {loading ? (
            <p className="text-gray-500">
              Loading...
            </p>
          ) : history.length === 0 ? (
            <p className="text-gray-500">
              No chat history found.
            </p>
          ) : (
            history.map((chat, index) => (
              <div
                key={index}
                className="mb-5 p-4 rounded-xl border bg-gray-50"
              >
                <h3 className="font-semibold text-blue-600">
                  Question
                </h3>

                <p className="text-sm mt-1">
                  {chat.question}
                </p>

                <h3 className="font-semibold text-green-600 mt-3">
                  Answer
                </h3>

                <p className="text-sm mt-1 whitespace-pre-wrap">
                  {chat.answer}
                </p>

              </div>
            ))
          )}

        </div>

        {/* Footer */}
        <div className="border-t p-5 flex gap-3">

          <button
            onClick={handleClear}
            className="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl flex items-center justify-center gap-2"
          >
            <Trash2 size={18} />
            Clear
          </button>

          <button
            onClick={handleExport}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl flex items-center justify-center gap-2"
          >
            <Download size={18} />
            Export
          </button>

        </div>

      </div>

    </div>
  );
}

export default HistoryPanel;