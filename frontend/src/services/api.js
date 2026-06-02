const API_URL = "https://signspeak-ai-backend-3c3g.onrender.com";

export async function checkBackend() {
  const response = await fetch(API_URL);
  return response.json();
}