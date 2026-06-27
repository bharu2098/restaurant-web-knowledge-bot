// src/services/api.js

const BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

/**
 * Generic API Request Helper
 */
async function apiRequest(endpoint, options = {}) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    const contentType = response.headers.get("content-type");

    let data = null;

    if (contentType && contentType.includes("application/json")) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      throw new Error(
        data?.detail ||
          data?.message ||
          "Something went wrong."
      );
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/* ===========================================================
   Upload PDF
=========================================================== */

export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest("/upload/", {
    method: "POST",
    body: formData,
  });
}

/* ===========================================================
   Load Website
=========================================================== */

export async function loadWebsite(url) {
  return apiRequest("/website/load", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url,
    }),
  });
}

/* ===========================================================
   Chat
=========================================================== */

export async function sendMessage(
  question,
  provider = "gemini"
) {
  return apiRequest("/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      provider,
    }),
  });
}

/* ===========================================================
   Chat History
=========================================================== */

export async function getHistory() {
  return apiRequest("/history/");
}

/* ===========================================================
   Clear History
=========================================================== */

export async function clearHistory() {
  return apiRequest("/history/", {
    method: "DELETE",
  });
}

/* ===========================================================
   Export Chat History
=========================================================== */

export function exportHistory() {
  window.open(
    `${BASE_URL}/history/export`,
    "_blank"
  );
}

/* ===========================================================
   Health Check (Optional)
=========================================================== */

export async function healthCheck() {
  return apiRequest("/health");
}