const form =
    document.getElementById("chat-form");

const input =
    document.getElementById("chat-input");

const messages =
    document.getElementById("chat-messages");


function addMessage(text, sender) {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        sender === "user"
            ? "flex justify-end"
            : "flex justify-start";

    const bubble =
        document.createElement("div");

    bubble.className =
        sender === "user"
            ? "message-user rounded-2xl px-5 py-4 max-w-[75%]"
            : "message-ai rounded-2xl px-5 py-4 max-w-[75%]";

    bubble.textContent = text;

    wrapper.appendChild(bubble);
    messages.appendChild(wrapper);

    messages.scrollTop =
        messages.scrollHeight;
}


form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        if (!requireAuth()) return;

        const message =
            input.value.trim();

        if (!message) return;

        addMessage(message, "user");

        input.value = "";

        try {

            const data =
                await apiFetch("/chat/", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })

                });

            addMessage(
                data.response,
                "ai"
            );

        } catch (error) {

            console.error(error);

            addMessage(
                "I'm unable to connect right now.",
                "ai"
            );

        }

    }
);