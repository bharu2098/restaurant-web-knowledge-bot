import {
  MapPin,
  Phone,
  Mail,
  Clock,
} from "lucide-react";

function Contact() {
  return (
    <section
      id="contact"
      className="py-24 bg-gray-100"
    >
      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-14">

          <h2 className="text-4xl font-bold text-gray-800">
            Contact Us
          </h2>

          <p className="mt-4 text-gray-600">
            We'd love to hear from you.
          </p>

        </div>

        <div className="grid md:grid-cols-2 gap-10">

          <div className="bg-white rounded-2xl shadow-md p-8 space-y-6">

            <div className="flex gap-4">

              <MapPin className="text-orange-500" />

              <div>

                <h3 className="font-semibold">
                  Address
                </h3>

                <p className="text-gray-600">
                  123 Food Street,
                  Hyderabad,
                  Telangana
                </p>

              </div>

            </div>

            <div className="flex gap-4">

              <Phone className="text-orange-500" />

              <div>

                <h3 className="font-semibold">
                  Phone
                </h3>

                <p className="text-gray-600">
                  +91 9876543210
                </p>

              </div>

            </div>

            <div className="flex gap-4">

              <Mail className="text-orange-500" />

              <div>

                <h3 className="font-semibold">
                  Email
                </h3>

                <p className="text-gray-600">
                  info@xoticrestaurant.com
                </p>

              </div>

            </div>

            <div className="flex gap-4">

              <Clock className="text-orange-500" />

              <div>

                <h3 className="font-semibold">
                  Opening Hours
                </h3>

                <p className="text-gray-600">
                  Mon - fri: 10:00 AM - 10:00 PM
                  sat- sun:  10:00 AM - 11:00 PM
                </p>

              </div>

            </div>

          </div>

          <div className="rounded-2xl overflow-hidden shadow-md">

            <iframe
              title="Restaurant Location"
              className="w-full h-full min-h-[450px]"
              src="https://maps.google.com/maps?q=Hyderabad&t=&z=13&ie=UTF8&iwloc=&output=embed"
            />

          </div>

        </div>

      </div>
    </section>
  );
}

export default Contact;