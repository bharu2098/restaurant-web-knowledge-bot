import {
  Bot,
  Database,
  Cpu,
  ShieldCheck,
} from "lucide-react";

function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-8 py-5 flex items-center justify-between shadow-sm">

      {/* Left */}
      <div className="flex items-center gap-4">

        <div className="w-14 h-14 rounded-xl bg-blue-100 flex items-center justify-center">

          <Bot
            className="text-blue-600"
            size={30}
          />

        </div>

        <div>

          <h1 className="text-3xl font-bold text-gray-800">
            Restaurant Knowledge Bot
          </h1>

          <p className="text-gray-500 mt-1">
            Website RAG • PDF RAG • Hybrid Search • AI Assistant
          </p>

        </div>

      </div>

      {/* Right */}
      <div className="flex items-center gap-3">

        {/* Knowledge Base */}
        <div className="flex items-center gap-2 bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-medium">

          <Database size={16} />

          <span>Knowledge Ready</span>

        </div>

        {/* AI Model */}
        <div className="flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium">

          <Cpu size={16} />

          <span>Gemini / Groq</span>

        </div>

        {/* Hybrid Search */}
        <div className="flex items-center gap-2 bg-purple-100 text-purple-700 px-4 py-2 rounded-full text-sm font-medium">

          <ShieldCheck size={16} />

          <span>Hybrid Search</span>

        </div>

      </div>

    </header>
  );
}

export default Header;