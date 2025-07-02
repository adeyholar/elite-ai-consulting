from services.ollama_client import OllamaClient
from services.pdf_generator import PDFGenerator
from datetime import datetime

class ReportAgent:
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.pdf_generator = PDFGenerator()

    def generate_report(self, task_id, desc):
        """
        Generate a report with AI analysis and save as PDF.
        """
        prompt = f"Provide a concise 200-300 word analysis for the task: '{desc}'. Return the response with clear paragraphs separated by double newlines (\\n\\n), avoiding excessive quotes or artifacts."
        analysis = self.ollama_client.generate(prompt, model="llama3.2:latest")
        title = f"Report for Task {task_id}: {desc}"
        # Ensure content has proper line breaks
        content = f"Task ID: {task_id}\nDescription: {desc}\n\nAnalysis:\n{analysis}"
        output_path = f"task_{task_id}.pdf"  # Relative path, will be prefixed with 'reports/'
        pdf_path = self.pdf_generator.create_pdf(content, output_path, title)
        return {
            'description': desc,
            'status': 'Completed',
            'ai_response': f"Report generated and saved as {pdf_path}",
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'pdf_path': pdf_path
        }