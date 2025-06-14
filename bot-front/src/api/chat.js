// src/api/chat.js
export async function sendMessageToRasa(message) {
  const res = await fetch("http://localhost:5005/webhooks/rest/webhook", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sender: "user123", // use a unique sender ID if needed
      message,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch from Rasa server");
  }

  return res.json(); // this returns an array of responses
}
