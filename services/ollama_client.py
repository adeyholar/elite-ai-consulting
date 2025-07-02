import requests
from config import OLLAMA_API_URL

class OllamaClient:
    def __init__(self):
        self.api_url = OLLAMA_API_URL

    def generate(self, prompt, model="llama3.3:70b", timeout=300):
        """
        Send a prompt to the specified Ollama model and return the response.
        Increased timeout to handle large model delays.
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.api_url, json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json().get("response", "Error: No response from model")
        except requests.RequestException as e:
            return f"Error generating response: {e}"