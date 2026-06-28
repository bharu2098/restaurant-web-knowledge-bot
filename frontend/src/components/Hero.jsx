import { UtensilsCrossed, Bot } from "lucide-react";

function Hero({ onOpenChat }) {
  const scrollToMenu = () => {
    const section = document.getElementById("menu");

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
      });
    }
  };

  return (
    <section
      id="home"
      className="bg-gradient-to-r from-orange-500 via-red-500 to-orange-600 text-white"
    >
      <div className="max-w-7xl mx-auto px-6 py-24">

        <div className="max-w-3xl">

          <div className="inline-flex items-center gap-2 bg-white/20 rounded-full px-4 py-2 mb-6">

            <UtensilsCrossed size={20} />

            <span className="font-medium">
              Welcome to Xotic Restaurant
            </span>

          </div>

          <h1 className="text-5xl md:text-6xl font-bold leading-tight">
            Fresh Food,
            <br />
            Amazing Taste.
          </h1>

          <p className="mt-6 text-lg md:text-xl text-orange-100 leading-8">
            Discover delicious dishes, premium ingredients,
            and a smarter dining experience powered by our
            AI Restaurant Assistant.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">

            <button
              onClick={scrollToMenu}
              className="bg-white text-orange-600 px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition"
            >
              Explore Menu
            </button>

            <button
              onClick={onOpenChat}
              className="flex items-center gap-2 border border-white px-8 py-4 rounded-xl hover:bg-white hover:text-orange-600 transition"
            >
              <Bot size={20} />

              Ask AI
            </button>

          </div>

        </div>

      </div>
    </section>
  );
}

export default Hero;