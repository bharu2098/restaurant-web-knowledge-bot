// src/services/api.js

const BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

/* ==========================================================
   Generic API Request Helper
========================================================== */

async function apiRequest(endpoint, options = {}) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    let data;

    const contentType =
      response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      throw new Error(
        data?.detail ||
        data?.message ||
        data ||
        "Something went wrong."
      );
    }

    return data;

  } catch (error) {
    console.error("API Error:", error);

    return {
      success: false,
      error: error.message || "Network Error",
    };
  }
}

/* ==========================================================
   Upload PDF
========================================================== */

export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest("/upload/", {
    method: "POST",
    body: formData,
  });
}

/* ==========================================================
   Load Website
========================================================== */

export async function loadWebsite(url) {
  return apiRequest("/website/load", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });
}

/* ==========================================================
   Chat
========================================================== */

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

/* ==========================================================
   Chat History
========================================================== */

export async function getHistory() {
  return apiRequest("/history/");
}

/* ==========================================================
   Clear History
========================================================== */

export async function clearHistory() {
  return apiRequest("/history/", {
    method: "DELETE",
  });
}

/* ==========================================================
   Export Chat
========================================================== */

export function exportHistory() {
  window.open(
    `${BASE_URL}/history/export`,
    "_blank"
  );
}

/* ==========================================================
   Health Check
========================================================== */

export async function healthCheck() {
  return apiRequest("/health");
}