import { FileText, Globe } from "lucide-react";

function SourceBadge({ source }) {
  if (!source) return null;

  const isWebsite = source.type === "Website";

  return (
    <div
      className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium mr-2 mt-2 ${
        isWebsite
          ? "bg-green-100 text-green-700"
          : "bg-blue-100 text-blue-700"
      }`}
    >
      {isWebsite ? (
        <Globe size={14} />
      ) : (
        <FileText size={14} />
      )}

      {isWebsite ? (
        <span className="truncate max-w-[220px]">
          Website
        </span>
      ) : (
        <span className="truncate max-w-[220px]">
          {source.file}
          {source.page && ` • Page ${source.page}`}
        </span>
      )}
    </div>
  );
}

export default SourceBadge;