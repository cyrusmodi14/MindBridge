async function loadDashboard() {
    if (!requireAuth()) return;

    try {
        const data = await apiFetch("/dashboard/");

        document.getElementById("welcome-message").textContent =
            data.user_name
                ? `Welcome back, ${data.user_name}`
                : "Welcome back";

        document.getElementById("current-vibe").textContent =
            data.current_vibe || "No data yet";

        document.getElementById("overall-score").textContent =
            data.overall_score ?? "—";

        document.getElementById("latest-insight").textContent =
            data.latest_insight ||
            "Complete an assessment to receive insights.";

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);