import {
  UtensilsCrossed,
  ChefHat,
  Clock3,
  Star,
} from "lucide-react";

function About() {
  const features = [
    {
      icon: <ChefHat size={28} />,
      title: "Expert Chefs",
      description:
        "Our experienced chefs prepare every dish with fresh ingredients and authentic recipes.",
    },
    {
      icon: <Clock3 size={28} />,
      title: "Fast Service",
      description:
        "Enjoy quick food preparation and excellent customer service every day.",
    },
    {
      icon: <Star size={28} />,
      title: "Premium Quality",
      description:
        "We serve high-quality food with great taste and exceptional hygiene.",
    },
  ];

  return (
    <section
      id="about"
      className="py-24 bg-white"
    >
      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-16">

          <div className="inline-flex items-center gap-2 bg-orange-100 text-orange-600 px-4 py-2 rounded-full mb-5">

            <UtensilsCrossed size={18} />

            About Us

          </div>

          <h2 className="text-4xl font-bold text-gray-800">
            Delicious Food,
            Memorable Experience
          </h2>

          <p className="mt-6 text-gray-600 max-w-3xl mx-auto leading-8">
            Xotic Restaurant offers a unique dining experience with
            carefully prepared dishes, fresh ingredients, and
            outstanding hospitality. Whether you're dining with
            family or friends, we ensure every visit is memorable.
          </p>

        </div>

        <div className="grid md:grid-cols-3 gap-8">

          {features.map((feature, index) => (

            <div
              key={index}
              className="bg-gray-50 rounded-2xl p-8 shadow-sm hover:shadow-xl transition"
            >

              <div className="w-16 h-16 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 mb-6">

                {feature.icon}

              </div>

              <h3 className="text-2xl font-semibold text-gray-800 mb-4">

                {feature.title}

              </h3>

              <p className="text-gray-600 leading-7">

                {feature.description}

              </p>

            </div>

          ))}

        </div>

      </div>
    </section>
  );
}

export default About;