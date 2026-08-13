const API_BASE = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("access_token");
}

async function apiFetch(endpoint, options = {}) {
    const token = getToken();

    const headers = {
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        let error;

        try {
            error = await response.json();
        } catch {
            error = { detail: "Something went wrong." };
        }

        throw new Error(error.detail || "API request failed");
    }

    return response.json();
}