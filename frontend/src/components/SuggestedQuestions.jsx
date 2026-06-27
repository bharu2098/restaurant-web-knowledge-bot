import { Sparkles } from "lucide-react";

function SuggestedQuestions({ onQuestionClick }) {
  const questions = [
    "What are today's specials?",
    "Show me the vegetarian menu.",
    "What are your opening hours?",
    "Can I reserve a table online?",
    "Do you have gluten-free options?",
    "What desserts do you serve?",
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full text-center">

      {/* AI Icon */}
      <div className="w-20 h-20 rounded-full bg-blue-100 flex items-center justify-center mb-6">
        <Sparkles size={36} className="text-blue-600" />
      </div>

      {/* Welcome */}
      <h2 className="text-3xl font-bold text-gray-800 mb-2">
        Welcome to Restaurant AI
      </h2>

      <p className="text-gray-500 max-w-xl mb-8">
        Ask questions about menus, opening hours, dishes, reservations,
        or any information available in your uploaded PDFs and website.
      </p>

      {/* Suggestions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-3xl">

        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => onQuestionClick?.(question)}
            className="bg-white border border-gray-200 rounded-xl p-4 text-left hover:bg-blue-50 hover:border-blue-400 transition shadow-sm"
          >
            <p className="font-medium text-gray-700">
              {question}
            </p>
          </button>
        ))}

      </div>

    </div>
  );
}

export default SuggestedQuestions;