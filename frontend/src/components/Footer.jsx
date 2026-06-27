import {
  Heart,
  Code2,
} from "lucide-react";

function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 px-8 py-5">

      <div className="flex flex-col md:flex-row items-center justify-between gap-4">

        {/* Left */}
        <div>
          <h3 className="font-semibold text-gray-800">
            🍽 Restaurant Web Knowledge Bot
          </h3>

          <p className="text-sm text-gray-500">
            Team Gamma • GENAI Internship • Milestone Project
          </p>
        </div>

        {/* Center */}
        <div className="flex items-center gap-2 text-sm text-gray-600">

          <Code2 size={16} />

          <span>
            React + FastAPI + ChromaDB + Gemini + Groq
          </span>

        </div>

        {/* Right */}
        <div className="flex items-center gap-2 text-sm text-gray-500">

          <Heart
            size={16}
            className="text-red-500"
          />

          <span>© 2026 Team Gamma</span>

        </div>

      </div>

    </footer>
  );
}

export default Footer;