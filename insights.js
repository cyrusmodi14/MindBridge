let selectedMood = null;

document.querySelectorAll(".mood-button").forEach(button => {
    button.addEventListener("click", () => {

        document.querySelectorAll(".mood-button")
            .forEach(btn => btn.classList.remove("selected"));

        button.classList.add("selected");

        selectedMood = button.dataset.mood;
    });
});


document
    .getElementById("save-mood-button")
    .addEventListener("click", async () => {

        if (!requireAuth()) return;

        const energy =
            Number(
                document.getElementById("energy-slider").value
            );

        if (!selectedMood) {
            alert("Please select your mood.");
            return;
        }

        try {

            await apiFetch("/mood/", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    mood: selectedMood,
                    energy: energy
                })
            });

            document.getElementById("save-status").textContent =
                "Check-in saved successfully.";

        } catch (error) {

            console.error(error);

            document.getElementById("save-status").textContent =
                "Unable to save your check-in.";
        }
    });