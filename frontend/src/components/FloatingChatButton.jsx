import { MessageCircle } from "lucide-react";

function FloatingChatButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="
      fixed
      bottom-6
      right-6
      w-16
      h-16
      rounded-full
      bg-orange-500
      hover:bg-orange-600
      text-white
      shadow-2xl
      flex
      items-center
      justify-center
      transition
      z-50
      "
    >
      <MessageCircle size={30} />
    </button>
  );
}

export default FloatingChatButton;