import requests
import json
import time

class OllamaClient:
    def __init__(self, host="http://ollama:11434", timeout=60):
        self.host = host
        self.timeout = timeout

    def generate(self, prompt, model="llama3.2:latest"):
        url = f"{self.host}/api/chat"  # Changed from /api/generate to /api/chat
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],  # Adjusted for chat API format
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "No response from Ollama")
        except requests.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"

    def list_models(self):
        url = f"{self.host}/api/tags"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"Error listing models: {str(e)}"