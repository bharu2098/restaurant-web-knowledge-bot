import { useState } from "react";
import {
  Menu,
  X,
  Bot,
  UtensilsCrossed,
} from "lucide-react";

function Navbar({ onOpenChat }) {
  const [mobileMenu, setMobileMenu] = useState(false);

  const scrollTo = (id) => {
    const section = document.getElementById(id);

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
      });
    }

    setMobileMenu(false);
  };

  const navItems = [
    { name: "Home", id: "home" },
    { name: "Menu", id: "menu" },
    { name: "Gallery", id: "gallery" },
    { name: "About", id: "about" },
    { name: "Contact", id: "contact" },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white shadow-md">

      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">

        {/* Logo */}

        <div className="flex items-center gap-3">

          <div className="bg-orange-500 p-2 rounded-xl">

            <UtensilsCrossed
              className="text-white"
              size={24}
            />

          </div>

          <div>

            <h1 className="text-xl font-bold text-gray-800">
              Xotic Restaurant
            </h1>

            <p className="text-xs text-gray-500">
              AI Powered Restaurant
            </p>

          </div>

        </div>

        {/* Desktop Navigation */}

        <nav className="hidden md:flex items-center gap-8">

          {navItems.map((item) => (

            <button
              key={item.id}
              onClick={() => scrollTo(item.id)}
              className="text-gray-700 hover:text-orange-600 transition font-medium"
            >
              {item.name}
            </button>

          ))}

        </nav>

        {/* Right Buttons */}

        <div className="hidden md:flex items-center gap-3">

          <button
            onClick={onOpenChat}
            className="flex items-center gap-2 bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-xl transition"
          >
            <Bot size={18} />
            Ask AI
          </button>

        </div>

        {/* Mobile Button */}

        <button
          onClick={() => setMobileMenu(!mobileMenu)}
          className="md:hidden"
        >

          {mobileMenu ? (
            <X size={28} />
          ) : (
            <Menu size={28} />
          )}

        </button>

      </div>

      {/* Mobile Menu */}

      {mobileMenu && (

        <div className="md:hidden border-t bg-white shadow-lg">

          <div className="flex flex-col p-5 gap-5">

            {navItems.map((item) => (

              <button
                key={item.id}
                onClick={() => scrollTo(item.id)}
                className="text-left text-gray-700 hover:text-orange-600 font-medium"
              >
                {item.name}
              </button>

            ))}

            <button
              onClick={onOpenChat}
              className="mt-3 bg-orange-500 hover:bg-orange-600 text-white rounded-xl py-3 flex items-center justify-center gap-2"
            >
              <Bot size={18} />
              Ask AI
            </button>

          </div>

        </div>

      )}

    </header>
  );
}

export default Navbar;