import { useState } from "react";
import {
  Globe,
  Link,
  Loader2,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

import { loadWebsite } from "../services/api";

function WebsiteLoader() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleLoadWebsite = async () => {
    if (!url.trim()) return;

    try {
      setLoading(true);
      setError("");
      setSuccess("");

      const response = await loadWebsite(url);

      console.log(response);

      setSuccess("Website loaded successfully!");

      setUrl("");
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to load website.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6">

      {/* Header */}
      <div className="flex items-center gap-3 mb-5">

        <div className="bg-green-100 p-3 rounded-xl">
          <Globe className="text-green-600" size={24} />
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-800">
            Load Website
          </h2>

          <p className="text-sm text-gray-500">
            Import restaurant website content
          </p>
        </div>

      </div>

      {/* URL Input */}
      <div className="relative">

        <Link
          className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
          size={18}
        />

        <input
          type="url"
          placeholder="https://restaurant.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
        />

      </div>

      {/* Success */}
      {success && (
        <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">

          <CheckCircle className="text-green-600" size={18} />

          <span className="text-green-700 text-sm">
            {success}
          </span>

        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3 flex items-center gap-2">

          <AlertCircle className="text-red-600" size={18} />

          <span className="text-red-700 text-sm">
            {error}
          </span>

        </div>
      )}

      {/* Button */}
      <button
        onClick={handleLoadWebsite}
        disabled={!url || loading}
        className={`mt-6 w-full py-3 rounded-xl font-semibold transition flex items-center justify-center gap-2 ${
          url && !loading
            ? "bg-green-600 hover:bg-green-700 text-white"
            : "bg-gray-300 text-gray-500 cursor-not-allowed"
        }`}
      >
        {loading ? (
          <>
            <Loader2
              className="animate-spin"
              size={18}
            />
            Loading Website...
          </>
        ) : (
          <>
            <Globe size={18} />
            Load Website
          </>
        )}
      </button>

    </div>
  );
}

export default WebsiteLoader;