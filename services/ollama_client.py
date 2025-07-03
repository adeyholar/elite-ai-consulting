import requests
import json
import time
from config import OLLAMA_API_URL  # Import the config

class OllamaClient:
    def __init__(self, host=OLLAMA_API_URL, timeout=30):
        self.host = host
        self.timeout = timeout

    def generate(self, prompt, model="llama3.2:latest"):
        url = self.host  # e.g., http://ollama:11434/api/generate
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            # Adjust parsing based on Ollama 0.9.5 /api/generate response
            # Expected structure: {"model": "...", "created_at": "...", "response": "...", "done": true}
            return result.get("response", "No response from Ollama")
        except requests.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"

    def list_models(self):
        url = f"{self.host.rsplit('/api/', 1)[0]}/api/tags"  # Extract base URL and append /api/tags
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"Error listing models: {str(e)}"