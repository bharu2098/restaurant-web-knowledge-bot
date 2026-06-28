import { Star } from "lucide-react";

function FoodCard({
  image,
  name,
  description,
  price,
}) {
  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition duration-300">

      <img
        src={image}
        alt={name}
        className="w-full h-56 object-cover"
      />

      <div className="p-5">

        <div className="flex justify-between items-center">

          <h3 className="text-xl font-bold text-gray-800">
            {name}
          </h3>

          <div className="flex items-center gap-1 text-yellow-500">
            <Star size={16} fill="currentColor" />
            <span className="text-sm font-medium">
              4.8
            </span>
          </div>

        </div>

        <p className="text-gray-600 mt-3 leading-7">
          {description}
        </p>

        <div className="mt-5 flex justify-between items-center">

          <span className="text-2xl font-bold text-orange-600">
            ₹{price}
          </span>

          <button className="bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-xl transition">
            Order
          </button>

        </div>

      </div>

    </div>
  );
}

export default FoodCard;