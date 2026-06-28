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

      await loadWebsite(url);

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
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-4">

      {/* Header */}
      <div className="flex items-center gap-3 mb-4">

        <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
          <Globe
            className="text-green-600"
            size={22}
          />
        </div>

        <div>
          <h2 className="text-lg font-semibold text-gray-800">
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
          className="w-full h-12 pl-12 pr-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
        />

      </div>

      {/* Success */}
      {success && (
        <div className="mt-3 flex items-center gap-2 rounded-lg bg-green-50 border border-green-200 p-2">

          <CheckCircle
            className="text-green-600"
            size={18}
          />

          <span className="text-sm text-green-700">
            {success}
          </span>

        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-3 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 p-2">

          <AlertCircle
            className="text-red-600"
            size={18}
          />

          <span className="text-sm text-red-700">
            {error}
          </span>

        </div>
      )}

      {/* Button */}
      <button
        onClick={handleLoadWebsite}
        disabled={!url || loading}
        className={`mt-4 w-full h-11 rounded-xl font-semibold transition flex items-center justify-center gap-2 ${
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