import { useRef, useState } from "react";
import {
  FileText,
  Upload,
  CheckCircle,
  Loader2,
} from "lucide-react";

import { uploadPDF } from "../services/api";

function UploadPDF() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const inputRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];

    if (!selected) return;

    if (selected.type !== "application/pdf") {
      setError("Please select a PDF file.");
      setSuccess("");
      setFile(null);
      return;
    }

    setError("");
    setSuccess("");
    setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      setLoading(true);
      setError("");
      setSuccess("");

      await uploadPDF(file);

      setSuccess("PDF uploaded successfully!");
      setFile(null);

      if (inputRef.current) {
        inputRef.current.value = "";
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-4">

      {/* Header */}
      <div className="flex items-center gap-3 mb-4">

        <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
          <FileText
            className="text-blue-600"
            size={22}
          />
        </div>

        <div>
          <h2 className="text-lg font-semibold text-gray-800">
            Upload PDF
          </h2>

          <p className="text-sm text-gray-500">
            Upload restaurant menus or documents
          </p>
        </div>

      </div>

      {/* Upload Area */}
      <label className="border-2 border-dashed border-gray-300 rounded-xl h-36 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition">

        <Upload
          className="text-blue-600 mb-2"
          size={34}
        />

        <p className="font-medium text-gray-800">
          Click to choose a PDF
        </p>

        <p className="text-xs text-gray-500 mt-1">
          PDF files only
        </p>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileChange}
        />

      </label>

      {/* Selected File */}
      {file && (
        <div className="mt-3 flex items-center gap-2 rounded-lg bg-blue-50 border border-blue-200 p-2">

          <CheckCircle
            size={18}
            className="text-blue-600"
          />

          <span className="text-sm text-blue-700 truncate">
            {file.name}
          </span>

        </div>
      )}

      {/* Success */}
      {success && (
        <div className="mt-3 rounded-lg bg-green-50 border border-green-200 px-3 py-2 text-sm text-green-700">
          {success}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-3 rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className={`mt-4 w-full h-11 rounded-xl font-semibold flex items-center justify-center gap-2 transition ${
          !file || loading
            ? "bg-gray-300 text-gray-500 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 text-white"
        }`}
      >
        {loading ? (
          <>
            <Loader2
              className="animate-spin"
              size={18}
            />
            Uploading...
          </>
        ) : (
          <>
            <Upload size={18} />
            Upload PDF
          </>
        )}
      </button>

    </div>
  );
}

export default UploadPDF;