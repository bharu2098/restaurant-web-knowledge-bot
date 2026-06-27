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

      const response = await uploadPDF(file);

      console.log(response);

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
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6">

      {/* Header */}

      <div className="flex items-center gap-3 mb-5">

        <div className="bg-blue-100 p-3 rounded-xl">
          <FileText className="text-blue-600" size={24} />
        </div>

        <div>

          <h2 className="text-xl font-semibold">
            Upload PDF
          </h2>

          <p className="text-gray-500 text-sm">
            Upload restaurant menus, policies or documents
          </p>

        </div>

      </div>

      {/* Upload Area */}

      <label className="border-2 border-dashed border-gray-300 rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition">

        <Upload
          className="text-blue-600 mb-3"
          size={40}
        />

        <p className="font-medium">
          Click to choose a PDF
        </p>

        <p className="text-sm text-gray-500 mt-1">
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

        <div className="mt-5 bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">

          <CheckCircle
            className="text-green-600"
            size={18}
          />

          <span className="text-green-700 text-sm">
            {file.name}
          </span>

        </div>

      )}

      {/* Success */}

      {success && (

        <div className="mt-4 bg-green-100 text-green-700 border border-green-300 rounded-lg p-3 text-sm">

          {success}

        </div>

      )}

      {/* Error */}

      {error && (

        <div className="mt-4 bg-red-100 text-red-700 border border-red-300 rounded-lg p-3 text-sm">

          {error}

        </div>

      )}

      {/* Upload Button */}

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className={`mt-6 w-full py-3 rounded-xl font-semibold transition flex justify-center items-center gap-2 ${
          !file || loading
            ? "bg-gray-300 text-gray-500 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 text-white"
        }`}
      >
        {loading ? (
          <>
            <Loader2
              size={18}
              className="animate-spin"
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