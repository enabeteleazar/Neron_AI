// src/services/api.js

/* ===========================
   Configuration globale
=========================== */

// Base URL du backend
const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://192.168.1.56:5000";

// Endpoints centralisés
const ENDPOINTS = {
  system: "/api/system",
  docker: "/api/docker",
};

/* ===========================
   Client HTTP générique
=========================== */

async function apiFetch(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
      },
      ...options,
    });

    if (!response.ok) {
      console.error(
        `[API] Erreur ${response.status} sur ${endpoint}`
      );
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error(`[API] Exception sur ${endpoint}`, error);
    return null;
  }
}

/* ===========================
   Fonctions métier
=========================== */

// Système (CPU / RAM / Temp / Status)
export async function fetchSystem() {
  return await apiFetch(ENDPOINTS.system);
}

// Docker (containers, états, etc.)
export async function fetchDocker() {
  const data = await apiFetch(ENDPOINTS.docker);
  return Array.isArray(data) ? data : [];
}
S