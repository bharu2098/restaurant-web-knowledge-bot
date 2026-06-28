import FoodCard from "./FoodCard";

function Menu() {
  const foods = [
    {
      image:
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
      name: "Classic Burger",
      description:
        "Juicy grilled burger with cheese, lettuce and crispy fries.",
      price: 249,
    },
    {
      image:
        "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
      name: "Cheese Pizza",
      description:
        "Fresh mozzarella, tomato sauce and basil on crispy crust.",
      price: 399,
    },
    {
      image:
        "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=800",
      name: "Chicken Biryani",
      description:
        "Authentic dum biryani served with raita and salan.",
      price: 299,
    },
    {
      image:
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
      name: "Healthy Salad",
      description:
        "Fresh vegetables with house special dressing.",
      price: 199,
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
            Popular Menu
          </h2>

          <p className="mt-4 text-gray-600">
            Explore our customer's favorite dishes.
          </p>

        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

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