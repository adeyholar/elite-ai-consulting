from services.ollama_client import OllamaClient
from datetime import datetime

class BlogAgent:
    def __init__(self):
        self.ollama_client = OllamaClient()

    def generate_blog(self, desc):
        """
        Generate a blog post based on the task description.
        """
        prompt = f"Write a 200-word blog post on a productivity topic related to '{desc}'."
        response = self.ollama_client.generate(prompt, model="llama3.2:latest")
        return {
            'description': desc,
            'status': 'Completed',
            'ai_response': response,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }