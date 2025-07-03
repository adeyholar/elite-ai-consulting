# config.py
import os

# Load environment variables with defaults
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", "587")
EMAIL_FROM = os.getenv("EMAIL_FROM", "adengongo@gmail.com")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")  # Add this line