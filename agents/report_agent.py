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
        prompt = f"Provide a detailed analysis for the task: '{desc}'."
        analysis = self.ollama_client.generate(prompt, model="llama3.3:70b")
        title = f"Report for Task {task_id}: {desc}"
        content = f"Task ID: {task_id}\nDescription: {desc}\nAnalysis:\n{analysis}"
        output_path = f"reports/task_{task_id}.pdf"
        pdf_path = self.pdf_generator.create_pdf(content, output_path, title)
        return {
            'description': desc,
            'status': 'Completed',
            'ai_response': f"Report generated and saved as {pdf_path}",
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'pdf_path': pdf_path
        }