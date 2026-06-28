function Gallery() {
  const images = [
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=900",
    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=900",
    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=900",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=900",
    "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=900",
    "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=900",
  ];

  return (
    <section
      id="gallery"
      className="py-24 bg-white"
    >
      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-14">

          <h2 className="text-4xl font-bold text-gray-800">
            Restaurant Gallery
          </h2>

          <p className="mt-4 text-gray-600">
            Take a look at our delicious food and beautiful restaurant.
          </p>

        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

          {images.map((image, index) => (

            <div
              key={index}
              className="overflow-hidden rounded-2xl shadow-md"
            >

              <img
                src={image}
                alt="Restaurant"
                className="w-full h-72 object-cover hover:scale-110 transition duration-500"
              />

            </div>

          ))}

        </div>

      </div>
    </section>
  );
}

export default Gallery;