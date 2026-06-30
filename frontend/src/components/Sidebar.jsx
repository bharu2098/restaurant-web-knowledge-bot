import {
  History,
  Download,
  CheckCircle,
} from "lucide-react";

import { exportHistory } from "../services/api";

function Sidebar({
  setShowHistory,
}) {
  const handleExport = () => {
    exportHistory();
  };

  return (
    <aside className="w-72 bg-slate-900 text-white flex flex-col justify-between">

      {/* Logo */}
      <div>

        <div className="px-6 py-8 border-b border-slate-800">

          <h1 className="text-2xl font-bold flex items-center gap-2">
            🍽 Restaurant Bot
          </h1>

          <p className="text-sm text-slate-400 mt-2">
            AI Knowledge Assistant
          </p>

        </div>

        {/* Navigation */}
        <nav className="mt-6 px-4 space-y-2">

          {/* History */}
          <button
            onClick={() => setShowHistory(true)}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-800 transition"
          >
            <History size={20} />
            <span>History</span>
          </button>

          {/* Export Chat */}
          <button
            onClick={handleExport}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-800 transition"
          >
            <Download size={20} />
            <span>Export Chat</span>
          </button>

        </nav>

      </div>

      {/* Footer */}
      <div className="p-6 border-t border-slate-800">

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-2 text-green-400">

            <CheckCircle size={18} />

            <span className="text-sm font-medium">
              Backend Connected
            </span>

          </div>

          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>

        </div>

      </div>

    </aside>
  );
}

export default Sidebar;