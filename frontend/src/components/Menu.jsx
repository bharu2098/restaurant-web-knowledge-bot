import FoodCard from "./FoodCard";

function Menu() {
  const foods = [
    {
      image:
        "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=800",
      name: "Veg Biryani",
      description:
        "Fragrant basmati rice cooked with fresh vegetables and aromatic spices.",
      price: 280,
    },
    {
      image:
        "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=800",
      name: "Chicken Biryani",
      description:
        "Authentic Hyderabadi chicken dum biryani served with raita.",
      price: 350,
    },
    {
      image:
        "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=800",
      name: "Paneer Butter Masala",
      description:
        "Soft paneer cubes cooked in a rich and creamy tomato gravy.",
      price: 290,
    },
    {
      image:
        "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?w=800",
      name: "Paneer Tikka",
      description:
        "Grilled paneer cubes marinated with Indian spices.",
      price: 250,
    },
    {
      image:
        "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800",
      name: "Veg Spring Rolls",
      description:
        "Crispy spring rolls stuffed with fresh vegetables.",
      price: 180,
    },
    {
      image:
        "https://images.unsplash.com/photo-1527477396000-e27163b481c2?w=800",
      name: "Chicken Wings",
      description:
        "Juicy chicken wings seasoned with flavorful spices.",
      price: 320,
    },
    {
      image:
        "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800",
      name: "Butter Naan",
      description:
        "Soft tandoor-baked naan brushed with butter.",
      price: 50,
    },
    {
      image:
        "https://images.unsplash.com/photo-1605197161470-5e6dcb8dfe6f?w=800",
      name: "Gulab Jamun",
      description:
        "Soft milk dumplings soaked in delicious sugar syrup.",
      price: 120,
    },
    {
      image:
        "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800",
      name: "Ice Cream",
      description:
        "Refreshing ice cream served chilled.",
      price: 150,
    },
    {
      image:
        "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800",
      name: "Coca-Cola",
      description:
        "Classic chilled soft drink.",
      price: 60,
    },
    {
      image:
        "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=800",
      name: "Fresh Lime Soda",
      description:
        "Freshly prepared lime soda served chilled.",
      price: 90,
    },
    {
      image:
        "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=800",
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