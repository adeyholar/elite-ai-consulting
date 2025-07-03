from services.ollama_client import OllamaClient
from services.pdf_generator import PDFGenerator
from datetime import datetime
import os

class ReportAgent:
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.pdf_generator = PDFGenerator()

    def generate_report(self, task_id: str, desc: str) -> dict:
        """
        Generate a report with AI analysis and save as PDF.
        """
        prompt = f"Provide a concise 200-300 word analysis for the task: '{desc}'. Return the response with clear paragraphs separated by double newlines (\\n\\n), avoiding excessive quotes or artifacts."
        analysis = self.ollama_client.generate(prompt, model="llama3.2:latest")
        if "Error" in analysis:
            analysis = "Failed to generate AI analysis due to Ollama error."
        title = f"Report for Task {task_id}: {desc}"
        content = f"Task ID: {task_id}\nDescription: {desc}\n\nAnalysis:\n{analysis}"
        output_path = os.path.join(os.path.dirname(__file__), '..', 'reports', f"task_{task_id}.pdf")
        pdf_path = self.pdf_generator.create_pdf(content, output_path, title)
        if pdf_path is None:
            return {
                'description': desc,
                'status': 'Failed',
                'ai_response': f"Failed to generate report for task {task_id}",
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'pdf_path': None
            }
        absolute_pdf_path = os.path.abspath(pdf_path)
        return {
            'description': desc,
            'status': 'Completed',
            'ai_response': analysis,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'pdf_path': absolute_pdf_path
        }