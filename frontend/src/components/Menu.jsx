import FoodCard from "./FoodCard";

import vegBiryani from "../assets/veg biryani.jpg";
import chickenBiryani from "../assets/chicken biryani.jpg";
import paneerButterMasala from "../assets/panner butter masala.jpg";
import paneerTikka from "../assets/panner tikka.jpg";
import butterNaan from "../assets/butter-naan.jpg";
import bbqChickenWings from "../assets/bbq-chicken-wings.jpg";
import vegetableSpringRolls from "../assets/Vegetable-Spring-Rolls-.jpeg";
import iceCream from "../assets/ice cream.jpg";
import mangoShake from "../assets/mango shake.jpg";
import cocaCola from "../assets/coca cola.jpg";
import freshLimeSoda from "../assets/fresh lime soda.jpg";
import gulabJamun from "../assets/gulab-jamun.jpg";


function Menu() {
  const foods = [
    {
      image: vegBiryani,
      name: "Veg Biryani",
      description:
        "Fragrant basmati rice cooked with fresh vegetables and aromatic spices.",
      price: 280,
    },
    {
      image: chickenBiryani,
      name: "Chicken Biryani",
      description:
        "Authentic Hyderabadi chicken dum biryani served with raita.",
      price: 350,
    },
    {
      image: paneerButterMasala,
      name: "Paneer Butter Masala",
      description:
        "Soft paneer cubes cooked in a rich and creamy tomato gravy.",
      price: 290,
    },
    {
      image: paneerTikka,
      name: "Paneer Tikka",
      description:
        "Grilled paneer cubes marinated with Indian spices.",
      price: 250,
    },
    {
      image: vegetableSpringRolls,
      name: "Veg Spring Rolls",
      description:
        "Crispy spring rolls stuffed with fresh vegetables.",
      price: 180,
    },
    {
      image: bbqChickenWings,
      name: "Chicken Wings",
      description:
        "Juicy chicken wings seasoned with flavorful spices.",
      price: 320,
    },
    {
      image: butterNaan,
      name: "Butter Naan",
      description:
        "Soft tandoor-baked naan brushed with butter.",
      price: 50,
    },
    {
      image: gulabJamun,
      name: "Gulab Jamun",
      description:
        "Soft milk dumplings soaked in delicious sugar syrup.",
      price: 120,
    },
    {
      image: iceCream,
      name: "Ice Cream",
      description:
        "Refreshing ice cream served chilled.",
      price: 150,
    },
    {
      image: cocaCola,
      name: "Coca-Cola",
      description:
        "Classic chilled soft drink.",
      price: 60,
    },
    {
      image: freshLimeSoda,
      name: "Fresh Lime Soda",
      description:
        "Freshly prepared lime soda served chilled.",
      price: 90,
    },
    {
      image: mangoShake,
      name: "Mango Shake",
      description:
        "Creamy mango milkshake made with fresh mangoes.",
      price: 140,
    },
  ];

  return (
    <section
      id="menu"
      className="py-24 bg-gray-100"
    >
      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-14">

          <h2 className="text-4xl font-bold text-gray-800">
            Our Menu
          </h2>

          <p className="mt-4 text-gray-600">
            Enjoy our delicious starters, main course, desserts and refreshing drinks.
          </p>

        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">

          {foods.map((food, index) => (
            <FoodCard
              key={index}
              image={food.image}
              name={food.name}
              description={food.description}
              price={food.price}
            />
          ))}

        </div>

      </div>
    </section>
  );
}

export default Menu;